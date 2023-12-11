

def clean_session(session):
    if 'order' in session.keys():
        del session['order']
    if 'payment_intent' in session.keys():
        del session['payment_intent']
    if 'session_id' in session.keys():
        del session['session_id']
    session.save()


def discount_percentages(price):
    if 20 < price <= 40:
        return 5
    elif 40 < price <= 60:
        return 10
    elif 60 < price <= 100:
        return 15
    elif 100 < price:
        return 20
