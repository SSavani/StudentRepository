#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

HW11 : Stevens Repo
Author: Savani Shivam
Date: 11/17/2019 2:00pm

"""

import os
from prettytable import PrettyTable
from collections import defaultdict
import sqlite3


class Student:
    """Student class to store student details"""

    def __init__(self, cwid, name, major):
        if cwid.strip() == "" or name.strip() == "" or major.strip() == "":
            raise ValueError(f"One of the (Cwid, name, major) arguments' value is missing (Cannot be empty) ")
        self.cwid = cwid
        self.name = name
        self.major = Major(major)
        self.courses = defaultdict(str)

    def add_course(self, course, grade=None):
        """Add courses the student has enrolled in"""
        if grade.strip() == "":
            grade = None
        self.courses[course] = grade

    def get_student_info(self):
        """get info for a single student"""
        return [self.cwid, self.name, self.major, self.courses]

        # if self.courses.items():
        #     # comp_courses, req_courses, elect_courses = self.major.completed_courses(self.courses)
        #     return [self.cwid, self.name, self.major, self.courses]
        # else:
        #     return [self.cwid, self.name, self.major, None]


class Major:
    """Major class to store details about courses in a major"""

    def __init__(self, major):
        self.major = major
        self.req = set()
        self.elect = set()

    def add_major(self, req_elec, course):
        """To add the req/elective courses """
        try:
            if req_elec != "R" and req_elec != "E":
                raise ValueError("Invalid course type")
            elif req_elec == "R":
                self.req.add(course)
            elif req_elec == "E":
                self.elect.add(course)
        except ValueError:
            print(f"Error: \n\t Invalid course type: {req_elec}")

    def get_major_info(self):
        """to get major info"""
        return [self.major, sorted(list(self.req)), sorted(list(self.elect))]

    def remaining_req(self, courses):
        """Return the remaining "Required" courses"""
        rem_req = self.req.difference(courses)
        if len(rem_req) == 0:
            return None
        else:
            return rem_req

    def remaining_elect(self, courses):
        """Return remaining elective courses"""
        rem_elect = self.elect.difference(courses)
        if len(rem_elect) < len(self.elect):
            return None
        else:
            return rem_elect

    def completed_courses(self, courses):
        """Return completed, remaining required and remaining elective courses"""
        comp_courses = set()
        valid_grades = ("A", "A-", "B+", "B", "B-", "C+", "C")
        for course, grade in courses.items():
            if grade is None:
                continue
            elif grade in valid_grades:
                comp_courses.add(course)

        rem_req = self.remaining_req(comp_courses)
        rem_elect = self.remaining_elect(comp_courses)

        return sorted(list(comp_courses)), rem_req, rem_elect


class Instructor:
    """Class to store details of instructors"""

    def __init__(self, cwid, name, dept):
        self.cwid = cwid
        self.name = name
        self.dept = dept
        self.courses = defaultdict(int)

    def add_course(self, course):
        """To add courses the instructor is teaching and num of students enrolled in it"""
        self.courses[course] += 1

    def get_instructor_info(self):
        """Get all info for a single instructor """
        instruct_info = []
        if self.courses.items():
            for course, stud_num in self.courses.items():
                instruct_info.append([self.cwid, self.name, self.dept, course, stud_num])
        else:
            instruct_info.append([self.cwid, self.name, self.dept, None, None])
        return instruct_info


class Repository:
    """Class to store all instances of students, instructors and grades"""

    def __init__(self, dir_path):
        try:
            os.chdir(dir_path)
        except FileNotFoundError:
            print("Error: \n \tPlease provide Valid directory!!", FileNotFoundError)

        self.dir_path = dir_path
        self.students_filepath = os.path.join(dir_path, "students.txt")
        self.instructors_filepath = os.path.join(dir_path, "instructors.txt")
        self.grades_filepath = os.path.join(dir_path, "grades.txt")
        self.majors_filepath = os.path.join(dir_path, "majors.txt")
        self.db_path = os.path.join(dir_path, "stevens.db")

        self.all_students = {}
        self.all_instructors = {}
        self.all_majors = {}

        self.read_files()  # call all read functions
        self.print_pt()  # call to print summary of students and instructors

    def read_files(self):
        """Function call To read files """
        self.read_students()
        self.read_instructors()
        try:
            self.read_grades()
        except ValueError as e:
            raise ValueError("Error in Reading Grades file", e)
        self.read_majors()

    def print_pt(self):
        """Function call to print summary"""
        self.major_prettytable()
        self.student_prettytable()
        self.instructor_prettytable()
        self.instructor_table_db(self.db_path)

    def file_reading_gen(self, filepath, sep, fields, header=True):
        """generator function to read tab separated text files and yield a list with all of the values
        from a single line in the file on each call to next()"""

        try:
            fp = open(filepath)
        except FileNotFoundError:
            print("Error:\n \tCannot Open File at", filepath)
        else:
            with fp:
                try:
                    line_numb = 0
                    for line in fp:
                        line_fields = tuple(line.rstrip('\n').split(sep))
                        line_numb += 1
                        if len(line_fields) != fields:
                            raise ValueError(
                                f"{filepath} has {len(line_fields)} fields on line {line_numb} but expected "
                                f"{fields}")
                        if header:
                            header = False
                            continue
                        else:
                            yield line.rstrip("\n").split(sep)
                except ValueError:
                    raise ValueError(
                        f"Error: \n\t{filepath} has {len(line_fields)} fields on line {line_numb} but expected "
                        f"{fields}")

    def read_students(self):
        """Read students.txt and store the (Key:CWID) and (Value:instance of Student class) in the dictionary"""
        for student in self.file_reading_gen(self.students_filepath, "\t", 3):
            cwid, name, major = student

            if cwid not in self.all_students:
                self.all_students[cwid] = Student(cwid, name, major)

    def read_instructors(self):
        """Read instructors.txt and store the (Key:CWID) and (Value:instance of Instructor class) in the dictionary"""
        for instructor in self.file_reading_gen(self.instructors_filepath, "\t", 3):
            cwid, name, dept = instructor
            if cwid not in self.all_instructors:
                self.all_instructors[cwid] = Instructor(cwid, name, dept)

    def read_grades(self):
        """Read grades.txt and update the grade of the course for given student and
        update the count of students enrolled in the course taught by the particular instructor """

        for grade_info in self.file_reading_gen(self.grades_filepath, "\t", 4):
            stud_cwid, course, grade, inst_cwid = grade_info
            try:
                if stud_cwid in self.all_students.keys():
                    self.all_students[stud_cwid].add_course(course, grade)
                else:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Error: \n \tCWID: '{stud_cwid}' of student not present in students database ")
            try:
                if inst_cwid in self.all_instructors.keys():
                    self.all_instructors[inst_cwid].add_course(course)
                else:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Error: \n \tCWID: '{inst_cwid}' of instructor not present in instructors database ")

    def read_majors(self):
        """Read majors.txt and store the courses accordingly"""
        for major, course_type, course in self.file_reading_gen(self.majors_filepath, "\t", 3):
            if major not in self.all_majors:
                self.all_majors[major] = Major(major)

            self.all_majors[major].add_major(course_type, course)

    def major_prettytable(self):
        """Print summary of Majors"""
        pt = PrettyTable(field_names=["Dept", "Required", "Electives"])
        for major in self.all_majors.values():
            dept, req_courses, elec_courses = major.get_major_info()
            pt.add_row([dept, req_courses, elec_courses])

        print("\nMajors Summary")
        print(pt)

    def student_prettytable(self):
        """Print summary of students"""
        pt = PrettyTable(field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required",
                                      "Remaining Electives"])
        for student in self.all_students.values():
            try:
                cwid, name, major, courses = student.get_student_info()
                if major.major not in self.all_majors.keys():
                    raise ValueError
                else:
                    comp, req, elect = self.all_majors[major.major].completed_courses(courses)
                    pt.add_row([cwid, name, major.major, comp, req, elect])
            except ValueError:
                print(f"Error: \n\t Unknown Major:'{major.major}' for student with CWID: {cwid}")

        print("\nStudent Summary")
        print(pt)

    def instructor_prettytable(self):
        """Print summary of Instructors"""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for instructor in self.all_instructors.values():
            for info in instructor.get_instructor_info():
                pt.add_row(info)

        print("\nInstructor Summary")
        print(pt)
        return pt

    def instructor_table_db(self, db_path):
        """Print instructor summary from database"""
        try:
            db = sqlite3.connect(db_path)
            pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
            query = "select instructors.CWID, instructors.Name, instructors.Dept, grades.Course, " \
                    "COUNT(grades.StudentCWID) as Num_Students from instructors join grades on CWID = InstructorCWID " \
                    "group by CWID,Course order by CWID DESC, Num_Students DESC ;"
            for row in db.execute(query):
                pt.add_row(row)
            print("\nInstructor Summary from Database")
            print(pt)
            return pt
        except sqlite3.OperationalError as e:
            print("Database Error: ", e)


def main():
    # path = "C:\\Users\shiva\Desktop\StudentRepository-HW10_git\StudentRepository-HW10\HW10"
    path = "C:\Stevens CS\sem3\810 Python prog\Assignments\HW11"
    try:
        repo_stevens = Repository(path)
    except ValueError as e:
        print("Value Error:", e)
    except FileNotFoundError as e:
        print("File not Found Error", e)


if __name__ == "__main__":
    main()
