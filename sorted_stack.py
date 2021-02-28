class students:
        def __init__(self, id, first_name, last_name, age, gender, average):
            self.id = id
            self.first_name = first_name
            self.last_name = last_name
            self.age = age
            self.gender = gender
            self.average = average

        def get_avg(self):
            return self.average

        def get_detalis(self):
            return 'id:' + str(self.id) + '\n' + 'first name: ' + self.first_name + '\n' + 'last name: ' + self.last_name + '\n' + 'age: ' + str(self.age) + '\n' + 'gender: ' + str(self.gender) + '\n' + 'average: ' + str(self.average)


def id_is_vaild(id):
    if len(str(id)) == 9:
        return True
    else:
        False

def cheak_age(age):
    if age<0:
        return False
    else: return True

def cheak_gender(gender):
    if gender == 0 or gender == 1:
        return True
    else: return False

def check_avg(average):
    if average <= 100 and average >= 0:
        return True
    else: return False



class sorted_stack:
    def __init__(self):
        self.sorted_stuck = []

    def isEmpty(self):
        return self.sorted_stuck ==  []

    def size(self):
        return len(self.sorted_stuck)

    def push(self,id, first_name, last_name,age,gender,average):
        if not id_is_vaild(id):
            print('id not vaild')
        elif not cheak_age(age):
            print('age can not be negative')
        elif not cheak_gender(gender):
            print('gender is not vaild. female - 0 ; men - 1')
        elif not check_avg(average):
            print('averge is not vaild plz enter num between 0-100')
        else:
            student = students(id,first_name,last_name,age,gender,average)
            self.sorted_stuck.append(student)
            self.sorted_stuck.sort(key=lambda i: i.average, reverse=True)


    def pop(self):
        temp =  self.sorted_stuck.pop()
        return students.get_detalis(temp)

    def top(self):
        temp = self.sorted_stuck[0]
        return students.get_detalis(temp)


