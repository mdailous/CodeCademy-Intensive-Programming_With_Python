class DuplicateISBNException(Exception):
    """Exception raised when a book is added with the same isbn as another book and a different title"""
    pass


class User(object):
    """User of the Tome Rater book reading and rating application."""
    def __init__(self, name, email):
        if type(name) != str:
            raise ValueError("name must be a string")
        if not self.__validate_email(email):
            raise ValueError("invalid email address specified")
        self.name = name
        self.email = email
        self.books = {}

    def __repr__(self):
        return "User {name} with email {email} has read {count} books".format(name=self.name,
                                                                              email=self.email,
                                                                              count=len(self.books))

    def __hash__(self):
        return hash((self.name, self.email))

    def __eq__(self, other):
        return self.__is_user(other) and self.name == other.name and self.email == other.email

    def __lt__(self, other):
        return self.__is_user(other) and self.name < other.name

    def __le__(self, other):
        return self.__is_user(other) and self.name <= other.name

    def __gt__(self, other):
        return self.__is_user(other) and self.name > other.name

    def __ge__(self, other):
        return self.__is_user(other) and self.name >= other.name

    def __is_user(self, other):
        """Validates the specified object is a User object"""
        return other is not None and type(other) == User

    def __get_first_name(self):
        """Returns the first component of the specified name"""
        names = self.name.split()
        if len(names) > 1:
            return names[0]
        else:
            return self.name

    def __get_last_name(self):
        """Returns the last component of the specified name"""
        names = self.name.split()
        if len(names) > 1:
            return names[-1]
        else:
            return self.name

    def __validate_email(self, email):
        """Verifies the email format as per the provided PDF documentation"""
        return email is not None and \
               type(email) == str and \
               ('@' in email) and \
               (email[email.rindex("."):] in ['.com', '.edu', '.org'])

    def get_name(self):
        """Returns the full name of the current user"""
        return self.name

    def get_email(self):
        """Returns the email address of the current user"""
        return self.email

    def change_email(self, email):
        """Updates the current user's email address"""
        if not self.__validate_email(email):
            raise ValueError("invalid email address specified")
        self.email = email
        print("{name}'s address has been updated to {email}".format(email=self.email,
                                                                    name=self.__get_first_name()))

    def read_book(self, book, rating=None):
        """Adds the specified book to the users list of read books"""
        self.books.update({book: rating})

    def get_average_rating(self):
        """Returns the average book rating across all books rated by the current user"""
        result = 0
        if len(self.books) > 0:
            ratings = [r for r in self.books.values() if r is not None]
            for rating in ratings:
                result += rating
            return result / len(ratings)
        else:
            return None

    def get_book_list(self):
        """Gets the list of books the current user has read"""
        return list(self.books.keys())


class Book(object):
    """Book object for the Tome Rater book reading and rating application."""
    def __init__(self, title, isbn, cost=0.00):
        if type(title) != str:
            raise ValueError("title must be a string")
        if type(isbn) != int:
            raise ValueError("isbn must be a number")
        if type(cost) != float and type(cost) != int:
            raise ValueError("cost must be a number")
        self.title = title
        self.isbn = isbn
        self.cost = cost
        self.ratings = []

    def __repr__(self):
        return "{title}".format(title=self.title)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __eq__(self, other):
        return self.__is_book(other) and self.title == other.title and self.isbn == other.isbn

    def __gt__(self, other):
        return self.__is_book(other) and self.title > other.title

    def __ge__(self, other):
        return self.__is_book(other) and self.title >= other.title

    def __lt__(self, other):
        return self.__is_book(other) and self.title < other.title

    def __le__(self, other):
        return self.__is_book(other) and self.title <= other.title

    def __is_book(self, other):
        """Verifies the specified object is a Book object"""
        return other is not None and (type(other) == Book or issubclass(type(other), Book))

    def get_cost(self):
        """Returns the cost associated with the current book"""
        return self.cost

    def set_cost(self, cost):
        """Sets the cost associated with the current book"""
        if type(cost) != float and type(cost) != int:
            raise ValueError("cost must be a number")
        self.cost = cost

    def get_title(self):
        """Returns the title of the current book"""
        return self.title

    def get_isbn(self):
        """Returns the ISBN number of the current book"""
        return self.isbn

    def set_isbn(self, isbn):
        """Sets the ISBN of the current book"""
        if type(isbn) != int:
            raise ValueError("isbn must be a number")
        self.isbn = isbn
        print("{title} has updated isbn to {isbn}".format(title=self.title,
                                                          isbn=self.isbn))

    def add_rating(self, rating):
        """Adds the specified rating to the current book"""
        if rating is not None:
            if type(rating) == int and (0 <= rating) and (rating <= 4):
                self.ratings.append(rating)
            else:
                print("Invalid rating")

    def get_average_rating(self):
        """Returns the average rating for the current book"""
        result = 0
        if len(self.ratings) > 0:
            ratings = [r for r in self.ratings if r is not None]
            for rating in ratings:
                result += rating
            return result / len(ratings)
        else:
            return None


class Fiction(Book):
    """Fiction Book for the Tome Rater book reading and rating application."""
    def __init__(self, title, author, isbn, cost=0.00):
        super().__init__(title, isbn, cost)
        if type(author) != str:
            raise ValueError("author must be a string")
        self.author = author

    def get_author(self):
        """Returns the author of this current fiction"""
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)


class Non_Fiction(Book):
    """Non-Fiction object for the Tome Rater book reading and rating application."""
    def __init__(self, title, subject, level, isbn, cost=0.00):
        super().__init__(title, isbn, cost)
        if type(subject) != str:
            raise ValueError("subject must be a string")
        if type(level) != str:
            raise ValueError("level must be a string")
        self.subject = subject

        self.level = level

    def get_subject(self):
        """Returns the subject of the non-fiction book"""
        return self.subject

    def get_level(self):
        """Returns the level of the non-fiction book"""
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title,
                                                               level=self.level,
                                                               subject=self.subject)


class TomeRater(object):
    """Main TomeRater application. This is where all the magic happens"""
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        rated_book_count = len([book for book in self.books.keys() if book.get_average_rating() is not None])
        return "{user_count} users have rated {book_count} books".format(user_count=
                                                                         len(self.users),
                                                                         book_count=rated_book_count)

    def __eq__(self, other):
        return self.__is_tomerater(other) and \
               len(self.users) == len(other.users) and \
               len(self.books) == len(other.books) and \
               self.users == other.users and \
               self.books == other.books

    def __is_tomerater(self, other):
        """Verifies the specified object is a TomRater object"""
        return other is not None and type(other) == TomeRater

    def __validate_book(self, book):
        """Validates the specified book has a unique ISBN number"""
        for current_book in self.books.keys():
            if (current_book.get_isbn() == book.get_isbn()) and (current_book != book):
                raise DuplicateISBNException(
                    "isbn is already associated with book {title}".format(title=book.get_title()))

    def __add_book_to_self(self, book):
        """Adds the specified book to the current TomeRater instance"""
        self.__validate_book(book)
        self.books.update({book: self.books.get(book, 0)})

    def create_book(self, title, isbn, cost=0.00):
        """Creates a new book based on the specified values"""
        result = Book(title, isbn, cost)
        self.__add_book_to_self(result)
        return result

    def create_novel(self, title, author, isbn, cost=0.00):
        """Creates a new fiction based on the specified values"""
        result = Fiction(title, author, isbn, cost)
        self.__add_book_to_self(result)
        return result

    def create_non_fiction(self, title, subject, level, isbn, cost=0.00):
        """Creates a new non-fiction based on the specified values"""
        result = Non_Fiction(title, subject, level, isbn)
        self.__add_book_to_self(result)
        return result

    def add_book_to_user(self, book, email, rating=None):
        """Adds the specified book to the specified user, if they exist"""
        if email not in self.users.keys():
            print("No user with email {email}!".format(email=email))
        else:
            user = self.users.get(email)
            user.read_book(book, rating)
            book.add_rating(rating)
            self.books.update({book: (self.books.get(book, 0) + 1)})

    def add_user(self, name, email, user_books=None):
        """Creates and adds a new user to the TomRater application, if they don't already exist"""
        if email in self.users.keys():
            print("User with email {email} already exists".format(email=email))
            return
        user = User(name, email)
        self.users.update({email: user})
        if user_books is not None:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        """Prints all of the books in the TomeRater catalog"""
        for book in self.books.keys():
            print(book)

    def print_users(self):
        """Prints all of the users in in the TomeRater application"""
        for user in self.users.keys():
            print(user)

    def most_read_book(self):
        """Returns the book that has been read by more users than any other"""
        if len(self.books) == 0:
            return None
        return [book for book, count in self.books.items() if count == max(list(self.books.values()))][0]

    def highest_rated_book(self):
        """Returns the book with the highest rating across all users"""
        if len(self.books) == 0:
            return None
        return [book for book in self.books.keys()
                if book.get_average_rating() == max(book.get_average_rating() for book in self.books.keys())][0]

    def most_positive_user(self):
        """Returns the user who has highly rated more books"""
        if len(self.users) == 0:
            return None
        return [user for user in self.users.values()
                if user.get_average_rating() == max(user.get_average_rating() for user in self.users.values())][0]

    def get_n_most_read_books(self, n):
        """Returns the first N books that have been read by more users that any other"""
        if type(n) != int:
            raise ValueError("n must be a number")
        if len(self.books) == 0:
            return None
        if n > len(self.books):
            n = len(self.books)
        return [item[1] for item in sorted(((value, key) for (key, value) in self.books.items()), reverse=True)][:n]

    def get_n_most_prolific_readers(self, n):
        """Returns the first N users that have read more books than any other user"""
        if type(n) != int:
            raise ValueError("n must be a number")
        if len(self.users) == 0:
            return None
        if n > len(self.users):
            n = len(self.users)
        return sorted(list(self.users.values()), key=lambda user: len(user.get_book_list()), reverse=True)[:n]

    def get_n_most_expensive_books(self, n):
        """Returns the first N books that cost the most"""
        if type(n) != int:
            raise ValueError("n must be a number")
        if len(self.books) == 0:
            return None
        if n > len(self.books):
            n = len(self.books)
        return sorted(list(self.books.keys()), key=lambda book: book.get_cost())[:n]

    def get_worth_of_user(self, email):
        """Returns the worth, in book cost, of the specified user"""
        if email not in self.users.keys():
            return "No user with email {email} exists".format(email=email)
        if len(self.users) == 0:
            return None
        return sum([book.get_cost() for book in self.users.get(email).get_book_list()])
