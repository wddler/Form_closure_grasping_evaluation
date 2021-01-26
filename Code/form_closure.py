#! /usr/bin/env python

import numpy as np
import math
from scipy.optimize import linprog
import os
import csv

#class for a contact
class Contact:
    def __init__(self, x, y, normal):
        self.x = x
        self.y = y
        self.normal = normal

#needed to read csv
cur_path = os.path.dirname(__file__)
new_path_open_form = os.path.relpath('..\\code\\open_form.csv', cur_path)
new_path_closed_form = os.path.relpath('..\\code\\closed_form.csv', cur_path)
new_path_output = os.path.relpath('..\\result\\output.txt', cur_path)

#read csv files with contacts not in form closure and make the list of Contact objects
open_form_contacts_list = []
with open(new_path_open_form, newline='') as contacts:
    contacts_reader = csv.reader(contacts)
    for row in contacts_reader:
        if row[0][0] == '#': #skip the strings with comments
            continue
        else:
            open_form_contacts_list.append(Contact(float(row[0]), float(row[1]), math.radians(float(row[2]))))

#read csv files with contacts not in form closure and make the list of Contact objects
closed_form_contacts_list = []
with open(new_path_closed_form, newline='') as contacts:
    contacts_reader = csv.reader(contacts)
    for row in contacts_reader:
        if row[0][0] == '#': #skip the strings with comments
            continue
        else:
            closed_form_contacts_list.append(Contact(float(row[0]), float(row[1]), math.radians(float(row[2]))))

contacts_matrix = [] #initialize a list for contacts matrix
#function to calculate the F vector (wrench)
def calc_F(contact): 
    f_x = round(math.cos(contact.normal),4)
    f_y = round(math.sin(contact.normal),4)
    p = np.array([[contact.x, contact.y, 0]])
    n = np.array([[f_x, f_y, 0]])
    m_z = np.cross(p, n)
    f = (m_z, f_x, f_y)
    contacts_matrix.append([m_z[0,2], f_x, f_y])
    return f

#implementation of a linear programming test with values corresponded to the example of the book
def calculate_form_closure(contacts_matrix):
    contacts_matrix = np.array(contacts_matrix).T
    f = np.array([1, 1, 1, 1])
    A = np.array([[-1,0,0,0], [0,-1,0,0], [0,0,-1,0], [0,0,0,-1]])
    b = np.array([-1, -1, -1, -1])
    F = contacts_matrix
    Aeq = F
    beq = np.array([0, 0, 0])
    k = linprog(f, A, b, Aeq, beq)
    if k.success == True:
        print('The body is in form closure')
    else:
        print('The body is not in form closure')
    print(k.x, '\n')
    return k.success, k.x
    
#call form closure calculation of contacts from open.csv
c1 = calc_F(open_form_contacts_list[0])
c2 = calc_F(open_form_contacts_list[1])
c3 = calc_F(open_form_contacts_list[2])
c4 = calc_F(open_form_contacts_list[3])
print('Calculating form closure for contacts in "open.csv"')
calculate_open_form = calculate_form_closure(contacts_matrix)

contacts_matrix = [] #makes empty list

#call form closure calculation of contacts from closed.csv
c1 = calc_F(closed_form_contacts_list[0])
c2 = calc_F(closed_form_contacts_list[1])
c3 = calc_F(closed_form_contacts_list[2])
c4 = calc_F(closed_form_contacts_list[3])
print('Calculating form closure for contacts in "closed.csv"')
calculate_closed_form = calculate_form_closure(contacts_matrix)


#functions to write information about contacts: coordinates and contact normal
def write_contacts(list_with_contacts):
    contact_id = 1 #local counter for contact id
    for contact_to_write in list_with_contacts:
        string_to_write = ("contact #", contact_id, "x:", contact_to_write.x, "y:", contact_to_write.x, "normal:", contact_to_write.normal)
        string_to_write = str(string_to_write) + "\n"
        output_file.write(string_to_write)
        contact_id = contact_id + contact_id

#write output text file
with open(new_path_output, mode='w') as output_file:
    output_file.write("This is the result of calculating form closure\n")
    output_file.write('\n')
    if calculate_open_form[0] == True:
        output_file.write("Contacts in 'open.csv' are: \n")
        write_contacts(open_form_contacts_list)
        output_file.write("The body with contacts in 'open.csv' IS IN form closure. The solution - 'k' vector is: \n")
        output_file.write(calculate_open_form[1], '\n')
    else:
        output_file.write("Contacts in 'open.csv' are: \n")
        write_contacts(open_form_contacts_list)
        output_file.write('The body with contacts in "open.csv" is NOT IN form closure.\n')
    output_file.write('\n')
    if calculate_closed_form[0] == True:
        output_file.write("Contacts in 'closed.csv' are: \n")
        write_contacts(closed_form_contacts_list)
        output_file.write("The body with contacts in 'closed.csv' IS IN form closure. The solution - 'k' vector is: \n")
        output_file.write((str(calculate_closed_form[1]) + '\n'))
    else:
        output_file.write("Contacts in 'closed.csv' are: \n")
        write_contacts(closed_form_contacts_list)
        output_file.write('The body with contacts in "closed.csv" is NOT IN form closure.\n')
    output_file.write('See the pictures for reference.\n')
    output_file.close()