from banking_api.banking_api_app.services import transfer_service


def is_user(request, user_id):
    if user_id is None or request.data.get('user_id') != user_id:
        return False
    return True


def is_employee(request, company_id):
    if company_id is None or request.data.get('company_id') != company_id:
        return False
    return True


def has_card(user_id, card_id):
    card = transfer_service.get_card(card_id)
    if user_id is None or card is None or card.user.id != user_id:
        return False
    return True
