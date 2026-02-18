from django.http import JsonResponse

from django.db.models import Q

def chat_api(request):
    if request.method == 'POST':
        message = request.POST.get('message', '').lower().strip()
        response_text = "I'm not sure how to help with that yet. Try asking about 'phones' or 'fashion'."
        products_data = []

        import re
        from store.models.product import Product

        # STOP WORDS to remove from search queries
        STOP_WORDS = {'show', 'me', 'products', 'find', 'looking', 'for', 'want', 'buy', 'add', 'to', 'cart', 'its', 'the', 'a', 'an', 'my', 'please', 'with', 'also', 'and', 'just', 'can', 'you'}
        
        # SYNONYM GROUPS for semantic search
        SYNONYM_GROUPS = [
            {'earbuds', 'earphones', 'airpods', 'headset', 'headphones', 'bluetooth', 'wireless', 'buds'},
            {'mobile', 'phone', 'smartphone', 'iphone', 'android', 'phones', 'mobiles', 'smartphones'},
            {'watch', 'smartwatch', 'band', 'wearable', 'watches'}
        ]

        # Clean message: Remove emojis and special chars (keep text, numbers, spaces)
        message = re.sub(r'[^\w\s\d]', '', message).strip()

        # 1. Check for "Add to Cart" command
        # Matches: "add iphone gold", "add iphone 256"
        cart_match = re.search(r'(?:add|buy)\s+(.*?)(?:\s+to\s+cart)?$', message, re.IGNORECASE)
        
        if cart_match and 'products' not in message: 
            raw_input = cart_match.group(1).replace('to cart', '').strip()
            
            # Split by "and", "also", "," to handle multiple items
            # Example: "iphone 13 and also its cover" -> ["iphone 13", "its cover"]
            sub_queries = re.split(r'\s+(?:and|also|,)\s+', raw_input)
            
            added_items = []
            
            for raw_query in sub_queries:
                raw_query = raw_query.strip()
                if not raw_query or raw_query in ['its', 'the']: continue # Skip filler words

                # Split into keywords
                keywords = [w for w in raw_query.split() if w.lower() not in STOP_WORDS]
                if not keywords: continue

                # Construct Strict Query (Must contain ALL keywords OR their synonyms)
                query = Q()
                for word in keywords:
                    # Expand word with synonyms
                    expanded_words = {word}
                    for group in SYNONYM_GROUPS:
                        if word.lower() in group:
                            expanded_words.update(group)
                    
                    # Create a sub-query for this word (Word OR Synonym1 OR Synonym2...)
                    word_q = Q()
                    for w in expanded_words:
                        if len(w) > 1:
                            word_q |= (Q(name__icontains=w) | Q(description__icontains=w) | Q(color__icontains=w) | Q(storage__icontains=w))
                    
                    # Combine with main query (AND logic between different keyword groups)
                    query &= word_q
                
                # Get all matches (not just first)
                candidates = list(Product.objects.filter(query))
                
                # Strict Filter for ADD command:
                valid_candidates = []
                for p in candidates:
                    name_lower = p.name.lower()
                    is_name_match = False
                    for w in keywords:
                        synonyms = {w}
                        for group in SYNONYM_GROUPS:
                             if w.lower() in group: synonyms.update(group)
                        
                        if any(s in name_lower for s in synonyms):
                            is_name_match = True
                            break
                    
                    if is_name_match:
                        valid_candidates.append(p)
                
                # Scoring Logic:
                def score_product(p):
                    score = 0
                    name_lower = p.name.lower()
                    for w in keywords:
                        synonyms = {w}
                        for group in SYNONYM_GROUPS:
                             if w.lower() in group: synonyms.update(group)
                        
                        if any(s in name_lower for s in synonyms):
                            score += 50 # Huge bonus for name match
                        
                        if p.color and w.lower() in p.color.lower():
                            score += 5
                            
                    score -= len(p.name)
                    return score

                valid_candidates.sort(key=score_product, reverse=True)
                product = valid_candidates[0] if valid_candidates else None
                
                if product:
                    # Add to Session Cart
                    cart = request.session.get('cart', {})
                    product_id = str(product.id)
                    
                    if product_id in cart:
                        cart[product_id] += 1
                    else:
                        cart[product_id] = 1
                    
                    request.session['cart'] = cart
                    added_items.append(product.name)

            if added_items:
                cart = request.session.get('cart', {})
                return JsonResponse({
                    'status': 'success',
                    'response': f"Done! I've added **{', '.join(added_items)}** to your cart. 🛒",
                    'action': 'update_cart',
                    'cart_length': len(cart),
                    'products': []
                })
            else:
                 response_text = f"I tried to find matching products keywords but found none. Try exact names."

        # 2. Check for "Price Under" filter
        # Matches: "phones under 50000"
        price_match = re.search(r'(?:under|below|less than)\s+(\d+)', message)
        
        if price_match:
            limit = int(price_match.group(1))
            # Extract keywords excluding the price part and stop words
            clean_message = re.sub(r'(?:under|below|less than)\s+(\d+)', '', message).strip()
            keywords = [w for w in clean_message.split() if w.lower() not in STOP_WORDS]
            
            query = Q(price__lte=limit)
            for word in keywords:
                # Expand synonyms
                expanded_words = {word}
                for group in SYNONYM_GROUPS:
                    if word.lower() in group:
                        expanded_words.update(group)
                
                word_q = Q()
                for w in expanded_words:
                    if len(w) > 1:
                        word_q |= (Q(name__icontains=w) | Q(description__icontains=w) | Q(category__name__icontains=w))
                query &= word_q
            
            matches = Product.objects.filter(query)[:5]
            if matches.exists():
                response_text = f"Here are some options under ₹{limit}:"
                for p in matches:
                     products_data.append({
                        'id': p.id,
                        'name': p.name,
                        'price': f"₹{p.price}",
                        'image': p.image.url if p.image else ''
                    })
            else:
                 response_text = f"I couldn't find anything under ₹{limit} matching your keywords. Try a higher budget?"

        # 3. Intent/Feature Search (Gaming, Camera, Battery, Budget)
        elif any(x in message for x in ['gaming', 'camera', 'battery', 'budget', 'cheap', 'photo', 'gamer']):
            
            intent_query = Q()
            intents_found = []
            
            # Gaming Intent
            if any(x in message for x in ['gaming', 'gamer', 'play']):
                intents_found.append("Gaming 🎮")
                # iPhones are great for gaming despite lower RAM numbers, so explicitly include them
                intent_query &= (Q(ram__icontains='8GB') | Q(ram__icontains='12GB') | Q(ram__icontains='16GB') | Q(description__icontains='gaming') | Q(name__icontains='iphone') | Q(name__icontains='apple'))

            # Camera Intent
            if any(x in message for x in ['camera', 'photo', 'selfie', 'shoot']):
                intents_found.append("Camera 📸")
                intent_query &= (Q(camera__icontains='64MP') | Q(camera__icontains='108MP') | Q(camera__icontains='200MP') | Q(camera__icontains='50MP') | Q(description__icontains='camera'))

            # Battery Intent
            if any(x in message for x in ['battery', 'backup', 'lasting']):
                intents_found.append("Big Battery 🔋")
                intent_query &= (Q(battery__icontains='5000') | Q(battery__icontains='6000') | Q(description__icontains='battery'))

            # Budget Intent
            if any(x in message for x in ['budget', 'cheap', 'affordable', 'low cost']):
                intents_found.append("Budget 💰")
                # Adjust budget based on context
                if 'gaming' in message:
                    intent_query &= Q(price__lte=20000)
                else:
                    intent_query &= Q(price__lte=15000)

            matches = Product.objects.filter(intent_query)[:5]
            
            if matches.exists():
                response_text = f"I found these excellent **{', '.join(intents_found)}** options for you:"
                for p in matches:
                     products_data.append({
                        'id': p.id,
                        'name': p.name,
                        'price': f"₹{p.price}",
                        'image': p.image.url if p.image else ''
                    })
            else:
                 response_text = f"I couldn't find any products matching those specific requirements ({', '.join(intents_found)}). Try relaxing the filters."

        # 5. Remove from Cart Check
        # Matches: "remove iphone", "delete samsung"
        remove_match = re.search(r'(?:remove|delete)\s+(.*?)(?:\s+from\s+cart)?$', message, re.IGNORECASE)
        if remove_match:
            raw_query = remove_match.group(1).replace('from cart', '').strip()
            keywords = [w for w in raw_query.split() if w.lower() not in STOP_WORDS]
            
            # Find product in cart to remove
            cart = request.session.get('cart', {})
            product_to_remove = None
            
            # Fetch all products currently in cart
            cart_ids = list(cart.keys())
            if cart_ids:
                cart_products = Product.objects.filter(id__in=cart_ids)
                
                # Use same scoring/matching logic to find WHICH item to remove
                # Strict scoring to ensure we don't remove wrong item
                best_score = -100
                
                for p in cart_products:
                    score = 0
                    name_lower = p.name.lower()
                    matches_keyword = False
                    
                    for w in keywords:
                        # minimal synonym check
                        if w.lower() in name_lower: 
                            score += 50
                            matches_keyword = True
                        elif p.color and w.lower() in p.color.lower():
                            score += 10
                            matches_keyword = True
                    
                    score -= len(p.name) # Prefer shorter/exact
                    
                    if matches_keyword and score > best_score:
                        best_score = score
                        product_to_remove = p

                if product_to_remove:
                    # Remove from session
                    cart.pop(str(product_to_remove.id))
                    request.session['cart'] = cart
                    
                    return JsonResponse({
                        'status': 'success',
                        'response': f"Done! Removed **{product_to_remove.name}** from your cart. 🗑️",
                        'action': 'update_cart',
                        'cart_length': len(cart),
                        'products': []
                    })
                else:
                    response_text = f"I couldn't find '{raw_query}' in your cart. You have {len(cart)} items."
            else:
                response_text = "Your cart is already empty!"

        # 6. Empty / Clear Cart Intent
        elif any(x in message for x in ['empty cart', 'clear cart', 'remove all', 'delete all']):
             request.session['cart'] = {}
             return JsonResponse({
                'status': 'success',
                'response': "Cart cleared! 🗑️ Start fresh?",
                'action': 'update_cart',
                'cart_length': 0,
                'products': []
             })

        # 7. Navigation / Page Redirects
        # Matches: "open cart", "go to checkout", "show orders"
        elif any(x in message for x in ['open', 'go to', 'show', 'redirect', 'checkout', 'pay']):
            redirect_url = None
            if 'cart' in message or 'bag' in message:
                response_text = "Opening your cart... 🛒"
                redirect_url = '/cart'
            elif 'checkout' in message or 'payment' in message or 'pay' in message or 'buy now' in message:
                response_text = "Proceeding to secure payment... 💳"
                redirect_url = '/payment'
            elif 'order' in message or 'history' in message:
                 response_text = "Redirecting to your orders... 📦"
                 redirect_url = '/orders'
            elif 'shop' in message or 'home' in message or 'store' in message:
                 response_text = "Taking you back to the store... 🏠"
                 redirect_url = '/'
            
            if redirect_url:
                return JsonResponse({
                    'status': 'success',
                    'response': response_text,
                    'action': 'redirect',
                    'url': redirect_url,
                    'products': []
                })

        # 7. FAQ & Utility Intents
        if not response_text: # Only check FAQ if no other intent matched
            if any(x in message for x in ['shipping', 'delivery', 'return', 'refund', 'track', 'order', 'contact', 'support']):
                if 'shipping' in message or 'delivery' in message:
                    response_text = "🚚 **Shipping Info**: We usually ship within 24 hours! Delivery takes 3-5 business days."
                elif 'return' in message or 'refund' in message:
                    response_text = "🔄 **Returns**: You can return any product within 30 days if you're not satisfied. No questions asked!"
                elif 'track' in message or 'order' in message:
                    response_text = "📦 **Order Tracking**: Your last order #ORD-9921 is currently **Out for Delivery**! It should arrive by 6 PM today."
                elif 'contact' in message or 'support' in message:
                     response_text = "📞 **Contact Us**: You can reach our support team at **support@eshop.com** or call 1-800-ESHOP."
                else:
                     response_text = "I can help with shipping, returns, or order tracking. What do you need to know?"

        # 8. Standard Keyword Search (Fallback)
        if not response_text or response_text.startswith("I'm not sure"):
             # Simulated AI Logic (Keyword Matching)
            if 'hello' in message or 'hi' in message:
                response_text = "Hello! tailored suggestions are my specialty. What are you looking for today?"
            elif 'help' in message:
                 response_text = "I can help you find products! Try typing 'phones under 50000' or 'add iphone gold'."
            elif 'thank' in message:
                 response_text = "You're welcome! Happy shopping! 🛍️"
            else:
                keywords = [w for w in message.split() if w.lower() not in STOP_WORDS]
                query = Q()
                for word in keywords:
                    # Expand synonyms
                    expanded_words = {word}
                    for group in SYNONYM_GROUPS:
                        if word.lower() in group:
                            expanded_words.update(group)
                            
                    word_q = Q()
                    for w in expanded_words:
                        if len(w) > 1: 
                            word_q |= (Q(name__icontains=w) | Q(description__icontains=w) | Q(category__name__icontains=w))
                    query &= word_q
                
                if query:
                    # Scoring Logic (Same as above)
                    candidates = list(Product.objects.filter(query))
                    
                    def score_product(p):
                        score = 0
                        name_lower = p.name.lower()
                        for k in keywords:
                            if k.lower() in name_lower: score += 10
                        score -= len(p.name)
                        return score

                    candidates.sort(key=score_product, reverse=True)
                    matches = candidates[:5]
                    
                    if matches:
                        response_text = f"I found some products for you:"
                        for p in matches:
                            products_data.append({
                                'id': p.id,
                                'name': p.name,
                                'price': f"₹{p.price}",
                                'image': p.image.url if p.image else ''
                            })
                    else:
                        response_text = "I couldn't find any products matching that description. Try broader keywords."
                else:
                    response_text = "I'm listening! Ask me about 'phones', 'watches', or filtered prices."

        return JsonResponse({'status': 'success', 'response': response_text, 'products': products_data})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
