from bs4 import BeautifulSoup
import requests
import sys


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
                        classes_and_requirements[degree[0]] = {
                            "Fall": [],
                            "Spring": []
                        }
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
                            for i in range(4):
                                fall_sem = []
                                spring_sem = []
                                fall_classes = all_leftpads[i].findAll('div', attrs={'class':'acalog-core'})[0].find('ul').findAll('li')
                                spring_classes = all_leftpads[i].findAll('div', attrs={'class':'acalog-core'})[1].find('ul').findAll('li')
                                if i == 0:
                                    index = 0
                                    while index < len(fall_classes):
                                        class_and_credits = fall_classes[index].get_text()
                                        try:
                                            test = class_and_credits.index(":")
                                            # Proceed with the logic if the colon is found
                                            # For example, split the string
                                            class_item = class_and_credits[0:test - 13]
                                            credits_per_class = class_and_credits[test + 2:test + 3]
                                            fall_sem.append(class_item + ":" + str(credits_per_class))
                                            index += 1
                                        except ValueError:
                                            # Skip the item or handle it in case of missing colon
                                            print("Colon not found, skipping this entry.")
                                            if class_and_credits == "or":
                                                or_classes = []
                                                fall_sem.pop(len(fall_sem) - 1)
                                                first_choice = fall_classes[index - 1].get_text()

                                                test = first_choice.index(":")
                                                # Proceed with the logic if the colon is found
                                                # For example, split the string
                                                class_item = first_choice[0:test - 13]
                                                credits_per_class = first_choice[test + 2:test + 3]
                                                or_classes.append(class_item + ":" + str(credits_per_class))

                                                second_choice = fall_classes[index + 1].get_text()
                                                test = second_choice.index(":")
                                                # Proceed with the logic if the colon is found
                                                # For example, split the string
                                                class_item = second_choice[0:test]
                                                credits_per_class = second_choice[test + 2:test + 3]
                                                or_classes.append(class_item + ":" + str(credits_per_class))
                                                fall_sem.append(or_classes)
                                                index += 2
                                            else:
                                                index += 1
                                    classes_and_requirements[degree[0]]["Fall"] = fall_sem
                                    print(classes_and_requirements)
                                    sys.exit(1)
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