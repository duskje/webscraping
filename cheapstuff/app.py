from websites import Banggood, Mercadolibre, Aliexpress
import mysql.connector
import click

# TODO: Switch to sqlite

@click.command()
@click.option('--search', '-s', help='Search Terms')
def main(search):
    websites = frozenset((
        Banggood(),
        Mercadolibre(),
    ))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password',
        database='junk_from_the_web'
    )

    sqL_cursor = conn.cursor()

    for site in websites:
        articles = site.get_articles(search_terms=search)

        for article in articles:
            article.save_into_database(sql_cursor=sqL_cursor, values=('title', 'url'))

    conn.commit()


if __name__ == '__main__':
    main()
