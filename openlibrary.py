import requests

def fetch_books_from_openlibrary(genre, description, max_results=5):
    """Fetch books from OpenLibrary based on genre and description."""
    query = f"{genre} {description}".strip()
    url = f"https://openlibrary.org/search.json?q={query}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        books = data.get('docs', [])
        results = []
        
        for book in books[:max_results]:
            languages = book.get('language', [])
            if 'eng' in languages:
                title = book.get('title', "Unknown Title")
                author = ', '.join(book.get('author_name', ["Unknown Author"]))
                year = book.get('first_publish_year', 'Unknown')
                book_url = f"https://openlibrary.org{book.get('key', '')}" if book.get('key') else "URL not available"
                cover_id= book.get('cover_i', None)
                if cover_id:
                    imglink = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                else:
                    # Attempt to use ISBN for cover image if cover_id is not available
                    isbn_list = book.get('isbn', [])
                    if isbn_list:
                        imglink = f"https://covers.openlibrary.org/b/isbn/{isbn_list[0]}-M.jpg"
                    else:
                        imglink = "Cover image not available"

                results.append({
                    "title": title,
                    "author": author,
                    "year": year,
                    "imglink": imglink,
                    "genre": genre,
                    "description": description,
                    "url": book_url
                })
        return results
    else:
        print("Failed to fetch books from OpenLibrary.")
        return []

genre=str(input("enter genre: "))
description=str(input("enter description: "))

response=''
while response !='n':
    results=fetch_books_from_openlibrary(genre, description)
    if not results:
        print("No more results found.")
        break

    for book in results:
        #variables make it to append it to sql table(BHAI BS INKA HI USE KAR TU!!)
        title=book['title']
        author=book['author']
        year=book['year']
        url=book['url']
        imglink=book['imglink']
        print(f"Title: {title}\n-->Author: {author}\n-->Year: {year}\n-->direct link: {url}\n-->imglink: {imglink}")
        #image link is just for testing
        response=str(input('do you want more results?(y/n): '))
        #default response is yes
