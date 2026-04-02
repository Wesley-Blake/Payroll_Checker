import validators

class EmailError(Exception):
    print("Email wasn't an email.")

class EmailList:
    def __init__(self):
        self.__email_list = []
        #if isinstance(email_list, list):
        #    for email in email_list:
        #        if validators.email(email):
        #            self.__email_list.append(email)
        #        else:
        #            raise EmailError
        #else:
        #    pass
    @property
    def email_list(self):
        return self.__email_list

    def append(self, email_input):
        if isinstance(email_input, str):
            if validators.email(email_input):
                self.__email_list.append(email_input)
            else:
                raise EmailError
        if isinstance(email_input, list):
            for email in email_input:
                if validators.email(email):
                    self.__email_list.append(email)
                else:
                    raise EmailError

if __name__ == '__main__':
    test = EmailList()
    print(test.email_list)

    test.append(['test@mail.com', 'other@mail.com'])
    print(test.email_list)
