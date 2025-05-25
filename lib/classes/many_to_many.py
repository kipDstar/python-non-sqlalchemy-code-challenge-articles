class Article:
    all = [] # class variable to hold all article instances created
    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Article title must be a string between 5 and 50 characters.")
        self._title = title
        self._author = None # none initially then set by the setter first because we need to validate 
        self._magazine = None # none initially then set by the setter
        
        self.author = author # set the author using this setter
        self.magazine = magazine # set the magazine using this setter which means it validates the magazine
        Article.all.append(self) # adds the article to the class variable all which holds all articles created

    @property
    def title(self):
        return self._title # returns the articles title
    @title.setter
    # to make title immutable
    def title(self, new_title):
        return AttributeError("Title is immutable and cannot be changed.")
    
    @property
    def author(self):
        return self._author # returns the author of the article
    
    @author.setter 
    def author(self, new_author):
        #from .many_to_many import Author  # Corrected import to avoid ModuleNotFoundError
        if not isinstance(new_author, Author):
            raise TypeError("Author must be an instance of Author class.")
        # a second check to ensure if the article is already assigned to an author it is removed from the previous author articles list
        if self._author is not None and self in self._author._articles:
            self._author._articles.remove(self)
        self._author = new_author
        # adds the article to the new author's articles list
        #additional check to see that no duplicates are added
        if self not in self._author._articles:
            self._author._articles.append(self) 
    
    @property 
    def magazine(self):
        return self._magazine # to return the magazine object of the article
    
    @magazine.setter
    def magazine(self, new_magazine):
        #from .many_to_many import Magazine  # Corrected import to avoid ModuleNotFoundError
        if not isinstance(new_magazine, Magazine):
            raise TypeError("Magazine must be an instance of the Magazine class.")
        #check to ensure if the article is already assigned to a magazine it is removed from the previous magazine articles list
        if self._magazine is not None and self in self._magazine._articles:
            self._magazine._articles.remove(self)
        self._magazine = new_magazine # assign the new magazine to the article
        if self not in self._magazine._articles:
            self._magazine._articles.append(self)
        # adds the article to the new magazine's articles list
        # checks also to see that no duplicates are added
    def __repr__(self):
        #return f"<Article Title: '{self.title}', Author: '{self.author.name}', Magazine: '{self.magazine.name}'>"
        author_name = self.author.name if self.author else "N/A"
        magazine_name = self.magazine.name if self.magazine else "N/A"
        return f"<Article Title: '{self.title}', Author: '{author_name}', Magazine: '{magazine_name}'>"
    
    # article should have all 

class Author:
    def __init__(self, name):
        # to validate the name
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self._name = name  # store the name in a private variable
        
        #next initialize an empty list to hold articles objects for the author
        self._articles = [] 
    
    @property  # to get the name of the author
    def name(self):
        return self._name
    # no name setter to make the name immutable
    
    def articles(self):
        return list(self._articles) # return the copy of the articles list to avoid directly modifing theoriginal list

    def magazines(self):
        # return a list of unique magazines the author wrote articles for
        unique_magazines = set() #set to handles unique magazines
        for article in self._articles:
            unique_magazines.add(article.magazine)
        return list(unique_magazines) #convert the set back to a list

    def add_article(self, magazine, title):
        # Create a new Article instance and associate it with this author and the given magazine
        new_article = Article(self, magazine, title)
        return new_article

    def topic_areas(self):
        # Return a list of unique categories for all magazines the author has written for
        if not self.magazines():
            return None # return an empty list if no magazines exist for the author
        unique_categories = set()
        for article in self._articles:
            unique_categories.add(article.magazine.category)
        return list(unique_categories) if unique_categories else [] #return list or empty list if no topic is found

    def __repr__(self):
        return f"<Author Name: '{self.name}'>" #string representation ofthe Author object

class Magazine:
    _all_magazines = [] # to hold all magazine instances
    def __init__(self, name, category):
        self.name = name
        self.category = category

        # empty list to hold articles for this magazine
        self._articles = []
        Magazine._all_magazines.append(self) # adds the magazine instance to the class variable holding all magazines

    @property #a getter for the name
    def name(self):
        return self._name #retruns name
    
    @name.setter # a setter for the name
    def name(self, value):
        if not isinstance(value, str):
            raise Exception("Magazine name must be a non-empty string.")
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value #assign the value to the private variable

    @property # a getter for the category
    def category(self):
        return self._category
    
    @category.setter # a setter for the category
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Magazine category must be a non-empty string.")
        if len(value) == 0:
            raise ValueError("Magazine category must be a non-empt string.")
        self._category = value #assigning the value to a private variable
    
    def articles(self):
        return list(self._articles)
    
    def contributors(self):
        # return a list of unique authors who have written articles for this magazine
        unique_contributors = set()
        for article in self._articles:
            unique_contributors.add(article.author)
        return list(unique_contributors) #convert uniue contibutors set to a list
       
    @classmethod 
    def all(cls):
        #this class method returns all nagazine instances created
        return cls._all_magazines

    def article_titles(self):
        # Return a list of title strings of all articles written for this magazine, and None if no articles exist
        if not self._articles: #to see if the mag has any articles
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        # Return a list of authors who have written more than 2 articles for this magazine
        #also return none if the mag has no authors with more than two articles published
        author_articles_count = {} # creates a dictionary to store an author object and the number of articles ppublished in a magazine as the value
        for article in self._articles:
            author = article.author
            author_articles_count[author] = author_articles_count.get(author, 0) + 1

        contributing_authors = []
        for author, count in author_articles_count.items():
            if count > 2:
                contributing_authors.append(author) #puts the author in the list if they have more than two articles published
        if not contributing_authors:
            return None
        return contributing_authors
    def __repr__(self):
        return f"<Magazine Name: '{self.name}', Category: '{self.category}'>"

# class method to return magazine instance with the most number of articles and it returns none if there are no articles across all magazines
    @classmethod
    def top_publisher(cls):
        if not cls._all_magazines:
            return None
        top_magazine = None
        max_articles = -1

        for magazine in cls._all_magazines:
            num_articles = len(magazine.articles())
            if num_articles > max_articles:
                max_articles = num_articles
                top_magazine = magazine
        if max_articles == 0 and top_magazine is not None:
            return None
        return top_magazine