import validators

class EmailList(dict):
    def __setitem__(self, key, value):
        if not validators.email(key):
            raise ValueError(f"Invalid email address: {key}")
        if not isinstance(value, list) or not all(validators.email(email) for email in value):
            raise ValueError(f"Value must be a list of valid email addresses: {value}")
        super().__setitem__(key, value)


if __name__ == "__main__":
    email_list = EmailList()
    #email_list["test1@example.com"] = ["test2@example.com", "test3@example.com"]
    email_list.update({"test1@example.com": []})
    email_list.update({"test1@example.com": ["test2@example.com", "test3@example.com"]})
    email_list["test1@example.com"] += ["test2@example.com", "test3@example.com"]

    print(email_list)
    email_list = EmailList()
    print(len(email_list))
