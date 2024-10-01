from bs4 import BeautifulSoup
import requests



# def main():
#     baseURL = 'https://glasswing.vc/our-companies/'
#     storage = []
#     pageToScrape = requests.get(baseURL)
#     while True:
#         if pageToScrape.status_code == 200:
#             soup = BeautifulSoup(pageToScrape.text, 'html.parser')
#             portfolios = soup.findAll('div', attrs={'class':'portfolio-card'})
#             for portfolio in portfolios:
#                 iteration = []
#                 helper(portfolio, iteration)
#                 storage.append(iteration)
#             break
#         else:
#             break
    
#     print("Updating values")
    
#     # file for csv
#     file_path = 'output.csv'

#     # Write data to the CSV file
#     with open(file_path, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(storage)


def main():
    print("Hello")
    URL = "https://catalog.rpi.edu/content.php?catoid=30&navoid=864"
    storage_p = []
    storage_ul = []
    pageToScrape = requests.get(URL)
    while True:
        if pageToScrape.status_code == 200:
            soup = BeautifulSoup(pageToScrape.text, 'html.parser')
            portfolios = soup.find('td', attrs={'class':'block_content', 'colspan':'2'})

            # get all the degree names
            p_names = portfolios.findAll('p', attrs={'style':'padding-left: 30px'})
            print(len(p_names))
            for name in p_names:
                strong = name.find('strong').get_text()
                print(strong)
                storage_p.append(strong)
            
            # get all the degree links and names of degrees
            degree_links = portfolios.findAll('ul', attrs={'class':'program-list'})
            for degree_type in degree_links:
                current_degrees = []
                list_degrees = degree_type.findAll('li', attrs={'style':'list-style-type: none'})
                for degree in list_degrees:
                    href = "https://catalog.rpi.edu/" + degree.find('a').get('href')
                    name = degree.find('a').get_text()
                    name_link_pair = [name, href]
                    current_degrees.append(name_link_pair)
                storage_ul.append(current_degrees)
        

            # time to visit individual links and find the credit requirements!
        break


if __name__ == "__main__":
    main()