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
        
            # - All the degrees in each type
            # print(storage_ul)
            # - Type of degrees
            # print(storage_p)
            # time to visit individual links and find the credit requirements!
            # use "acalog index % 3" to get the year, fall semester, and spring semester. 
    
            # more issues:
            # 1. Not all the pages are in the same format. You will indeed have a total of 8 acalog_core's and 4 headers per undergraduate degree (check COMD for the error)
            # 2. Try using a counter instead of intentionally shortening the acalog_core list. The code will need a lot of work.
            classes_and_requirements = {}
            for index_of_degree in range(len(storage_p)):
                # print(storage_ul[index_of_degree])
                # bachelors
                if storage_p[index_of_degree] == "Baccalaureate":
                    for degree in storage_ul[index_of_degree]:
                        classes_and_requirements[degree[0]] = {}
                        link = degree[1]
                        requirements = requests.get(link)
                        print(classes_and_requirements)
                        if requirements.status_code == 200:
                            soup = BeautifulSoup(requirements.text, 'html.parser')
                            portfolios = soup.find('td', attrs={'colspan':'4', 'class':'width' })
                            all_info = portfolios.find('div', attrs={'class':'custom_leftpad_20'})
                            # get all acalog-cores (first thru. fourth years)
                            all_acalog_cores = all_info.findAll('div', attrs={'class':'acalog-core'}, recursive=False)[0:4]
                            all_leftpads = all_info.findAll('div', attrs={'class':'custom_leftpad_20'}, recursive=False)[0:4]
                            # print(all_acalog_cores)
                            # print(all_leftpads)
                            fall_sem = []
                            spring_sem = []
                            for i in range(4):
                                fall_classes = all_leftpads[i].findAll('div', attrs={'class':'acalog-core'})[0].find('ul')
                                spring_classes = all_leftpads[i].findAll('div', attrs={'class':'acalog-core'})[1].find('ul')
                                print(fall_classes)
                                return
                                if i == 0:
                                    classes_and_requirements[degree[0]]["First Year"] = []
                                elif i == 1:
                                    classes_and_requirements[degree[0]]["Second Year"] = []
                                elif i == 2:
                                    classes_and_requirements[degree[0]]["Third Year"] = []
                                else:
                                    classes_and_requirements[degree[0]]["Fourth Year"] = []
                            # return
                        print(classes_and_requirements)

        break


if __name__ == "__main__":
    main()