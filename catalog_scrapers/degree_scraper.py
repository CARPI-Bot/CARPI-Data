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
            for name in p_names:
                strong = name.find('strong').get_text()
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
        
            # print(len(storage_ul))
            # print(storage_ul[0])
            # print(storage_p)
            # return
            # time to visit individual links and find the credit requirements!
            # use "acalog index % 3" to get the year, fall semester, and spring semester. 
            # will need to separate carefully to get the right information
            classes_and_requirements = {}
            for index_of_degree in range(len(storage_p)):
                # print(storage_ul[index_of_degree])
                # bachelors
                if storage_p[index_of_degree] == "Baccalaureate":
                    for degree in storage_ul[index_of_degree]:
                        classes_and_requirements[degree[0]] = []
                        link = degree[1]
                        requirements = requests.get(link)
                        if requirements.status_code == 200:
                            acalog_core_counter = 0
                            soup = BeautifulSoup(requirements.text, 'html.parser')
                            portfolios = soup.find('div', attrs={'class':'custom_leftpad_20'})
                            # get all acalog-cores
                            acalog_core = portfolios.findAll('div', attrs={'class':'acalog-core'})[0:13]
                            for i in range(len(acalog_core)):
                                # print(acalog_core[i])
                                if i >= 6:
                                    # junior year
                                    if i == 6:
                                        classes_and_requirements["Junior"] = []
                                    elif i <= 9:
                                        x = 5
                                    
                                    if i == 10:
                                        classes_and_requirements["Senior"] = []
                                    elif i > 10:
                                        x = 6
                                else:
                                    if i % 3 == 0:
                                        # year
                                        year = acalog_core[i].find('h2').get_text()
                                        if year == "First Year":
                                            classes_and_requirements["Freshman"] = []
                                        elif year == "Second Year":
                                            classes_and_requirements["Sophomore"] = []
                
                        print(classes_and_requirements)

        break


if __name__ == "__main__":
    main()