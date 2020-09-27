def is_user(request, user_id):
    if user_id is None or request.data.get('user_id') != user_id:
        return False
    return True


def is_employee(request, company_id):
    if company_id is None or request.data.get('company_id') != company_id:
        return False
    return True
