#It's time to learn how to manipulate data and write scripts for automation purposes!

#Know the basics of opening, reading, and writing to files.



#READING AND WRITING

       # test = open('test.txt','r')
#this connects python to this file (test.txt) on the hard drive for reading

#It doesn't actually read the words inside the file yet. 
# It just checks if the file exists, verifies your permissions, 
# and creates a file object (a stream).



#Once the stream is built, .read() is the tube that sucks the data out of the file 
#and dumps it into a Python variable.

    #text = test.read()
    #print(text)

#What it does: 
# It reads the entire file from start to finish, converts it a giant string,
#  and saves it into memory under the variable name text.

#"text" variable is now a string that can be manipulated


with open('test.txt', 'w') as f:
    f.write('Hi\n')
    f.write('Bye\n')
    f.write('see ya\n')
#this does the same thing but in a more efficient way! it calls the open function
#and saves it into a variable f in the same line.
#

with open('test.txt','r') as f:
    text = f.read()
    print(text)
#writing

#for char in f:
#print(char)
