import bs4
import asyncio  
import aiohttp
import json
import time
import lxml

async def get_subjects(session, term):
    subjects_dict = {}
    url = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses"
    url = f"{url}?term_in={term}&sel_crse_strt=&sel_crse_end=&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr="

    async with session.get(url) as response:
        soup = bs4.BeautifulSoup(await response.text(), "lxml")

        subjects = soup.find("select", {"name": "sel_subj"}).find_all("option")
        for subject in subjects:
            subject_code = subject.get("value")
            subject_name = subject.get_text()
            subjects_dict[subject_code] = subject_name

        return subjects_dict

async def get_courses(session, term, subject_code):   
    course_dict = {}
    url = "https://sis.rpi.edu/rss/bwckctlg.p_display_courses"
    params = f"term_in={term}&"\
            "call_proc_in=&"\
            "sel_subj=dummy&"\
            "sel_levl=dummy&"\
            "sel_schd=dummy&"\
            "sel_coll=dummy&"\
            "sel_divs=dummy&"\
            "sel_dept=dummy&"\
            "sel_attr=dummy&"\
            f"sel_subj={subject_code}&"\
            "sel_crse_strt=&"\
            "sel_crse_end=&"\
            "sel_title=&"\
            "sel_levl=%25&"\
            "sel_schd=%25&"\
            "sel_coll=%25&"\
            "sel_divs=%25&"\
            "sel_dept=%25&"\
            "sel_from_cred=&"\
            "sel_to_cred=&"\
            "sel_attr=%25"

    url = f"{url}?{params}"
    async with session.get(url) as response:
        start = time.time()
        soup = bs4.BeautifulSoup(await response.text(), "lxml")

        tasks = []

        subj_class_data = soup.find_all("td", class_="nttitle")
        for class_link in subj_class_data:
            class_link = class_link.find("a")
            class_code_name = class_link.get_text().split(" - ") # some class names include '-' 
            class_code, class_name = class_code_name[0], class_code_name[1]
            subject_code, course_code = class_code.split(" ")

            task = asyncio.create_task(get_sections(session, term, subject_code, course_code))
            tasks.append((task, class_code, class_name))

        results = await asyncio.gather(*[task for task, _, _ in tasks])

        for (task_result, (_, class_code, class_name)) in zip(results, tasks):
            if not task_result:
                course_dict[class_code] = class_name

        end = time.time()
        print(f"Time taken to get {subject_code}: {end - start} seconds")
        return course_dict
        
async def get_sections(session, term, subject_code, course_code):
    url = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse"
    params = f"term_in={term}&subj_in={subject_code}&crse_in={course_code}&schd_in=%"
    url = f"{url}?{params}"
    async with session.get(url) as response:
        soup = bs4.BeautifulSoup(await response.text(), "lxml")
        output = soup.find("caption", class_="captiontext")
        if(output == None):
            return None
        
def get_term(year, semester):
    if semester == "fall":
        return f"{year}09"
    elif semester == "spring":
        return f"{year}01"
    else:
        return None

async def main():
    total_start = time.time()
    # for i in range(2000, 2025):
    for i in range(2023, 2024):
        for semester in ["fall", "spring"]:
            term = get_term(i, semester)
            print(f"Term: {term}")
            async with aiohttp.ClientSession() as session:
                start = time.time() 
                subjects = await get_subjects(session, term=term)
                all_courses = {}

                tasks = []

                subject_metadata = []
                for subject_code, subject_name in subjects.items():
                    task = asyncio.create_task(get_courses(session=session, term=term, subject_code=subject_code))
                    tasks.append(task)
                    subject_metadata.append((subject_code, subject_name))

                courses_by_subject = await asyncio.gather(*tasks)
                for (subject_code, subject_name), courses in zip(subject_metadata, courses_by_subject):
                    all_courses[subject_code] = {
                        "subject_name": subject_name,
                        "courses": courses
                    }
                with open(f"./Data/{term}.json", "w") as f:
                    json.dump(all_courses, f, indent=4)
                end = time.time()
                print(f"Time taken: {end - start} seconds")

    total_end = time.time()
    print(f"Total time taken: {total_end - total_start} seconds")

if __name__ == "__main__":
    asyncio.run(main())