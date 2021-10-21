import re


def UserSignUpCred(link, login, password, tg_id: str):
    rows = link.Select('users', f"`login` = '{login}' AND `vis_pass` = '{password}'")
    if rows:
        user = rows[0]
        link.Update('users', {
            'tg_id': tg_id
        }, f"id={user['id']}")

        return True

    return False


def UserSignUpPhone(link, table, table2, phone, tg_id):
    rows = link.Select(f'{table}', f"`phone` = '{phone}'")
    if rows:
        user = rows[0]
        link.Update(f'{table2}', {
            'tg_id': f'{tg_id}'
        }, f"id={user['id']}")

        return True

    return False


def UserAuth(link, tg_id: str):
    rows = link.Select('users', f'`tg_id` = {tg_id}')
    return rows[0]


def LoadDB(users, link):
    for row in link.Select('users'):
        users[row['tg_id']] = {}
        users[row['tg_id']]['isAuth'] = True
        users[row['tg_id']]['typeuser'] = 'user'

    for row in link.Select('investors'):
        users[row['tg_id']] = {}
        users[row['tg_id']]['isAuth'] = True
        users[row['tg_id']]['typeuser'] = 'investors'

    for row in link.Select('work_drivers'):
        users[row['tg_id']] = {}
        users[row['tg_id']]['isAuth'] = True
        users[row['tg_id']]['typeuser'] = 'driver'


def GetNumber(text):
    phone = re.sub(r'[^0-9]', '', text, count=0)
    if len(phone) > 10:
        phone = phone[1:]
    return phone
