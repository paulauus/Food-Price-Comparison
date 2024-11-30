from subprocess import run

file_to_run = "scrapers/tesco_extract.py"
product_to_search = input("enter the name of the product: ")

if __name__ == '__main__':
    run(['python3', file_to_run, product_to_search])