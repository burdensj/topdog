import PySimpleGUI as sg
from datetime import date

dogs = {}


class Dog:
    def __init__(self, id_, name, breed, owner, date_joined):
        self.id_ = id_
        self.name = name
        self.breed = breed
        self.owner = owner
        self.date_joined = date_joined
        self.balance = 0

    def add_payment(self, payment):
        # TODO do some tests
        try:
            self.balance += int(payment)
        except:
            return False
        else:
            return self.balance

    def record_attendance(self):
        # TODO do some tests
        self.balance -= 10  # TODO make this a variable


# Add some example data
dogs['MAX0000'] = Dog(id_='MAX0000', name='Max', breed='Mixed', owner='Mum', date_joined='07/09/2019')
dogs['COOP0000'] = Dog(id_='COOP0000', name='Cooper', breed='Cockapoo', owner='Steve', date_joined='07/09/2019')
dogs['LILY0000'] = Dog(id_='LILY0000', name='Lily', breed='Border Collie', owner='Sam', date_joined='07/09/2019')


def main_screen(attendees=False):
    main_layout = [[sg.Text(label[0], size=(label[1], 1))
                    for label in (('', 3), ('Name', 10), ('Owner', 10), ('Breed', 10), ('Attended', 10))
                    ]]

    print(attendees)

    for dog in dogs.values():
        if attendees:
            attended = dog.id_ in attendees
        else:
            attended = False
        main_layout += [[sg.Radio('', 'DOG', key=('dog_id', dog.id_)),
                         sg.Text(dog.name, size=(10, 1), key=('name', dog.id_)),
                         sg.Text(dog.owner, size=(10, 1), key=('breed', dog.id_)),
                         sg.Text(dog.breed, size=(10, 1), key=('owner', dog.id_)),
                         sg.Checkbox(default=attended, text='', key=('attendance', dog.id_))
                         ]]

    main_layout += [[sg.Button('New'), sg.Button('Edit'), sg.Button('Record Attendance'), sg.Exit()]]

    main_window = sg.Window('Top Dog', main_layout)

    while True:
        event, values = main_window.Read()
        print(values)
        if event in (None, 'Exit'):
            break
        elif event == 'New':
            id_ = dog_edit(mode='new')
            print(id_)
            main_window.close()
            attendees = []
            for key, value in values.items():
                if key[0] == 'attendance' and value is True:
                    attendees += [key[1]]
            attendees += [id_]
            print(attendees)
            main_screen(attendees)
        elif event == 'Edit':
            success = False
            for key, value in values.items():
                if key[0] == 'dog_id' and value is True:
                    success = True
                    id_ = key[1]
                    name, breed, owner = dog_edit(mode='edit', id_=id_)
                    main_window[('name', id_)].Update(name)
                    main_window[('breed', id_)].Update(breed)
                    main_window[('owner', id_)].Update(owner)
            if success is False:
                raise ValueError('Couldn\'t find the dog')
        elif event == 'Record Attendance':
            for key, value in values.items():
                attendees = []
                if key[0] == 'attendance' and value is True:
                    attendees.append(key[1])

    main_window.close()


def dog_edit(mode='new', id_=''):

    if mode == 'new':
        name = ''
        breed = ''
        owner = ''
        date_joined = date.today().strftime('%d/%m/%Y')
        balance = 0
    elif mode == 'edit':
        dog = dogs[id_]
        name = dog.name
        breed = dog.breed
        owner = dog.owner
        date_joined = dog.date_joined
        balance = dog.balance
    else:
        raise ValueError('Incorrect mode provided')

    dog_edit_layout = [
        [sg.Text('Name', size=(16, 1)), sg.Input(key='name', focus=True, default_text=name, size=(30, 1))],
        [sg.Text('Breed', size=(16, 1)), sg.Input(key='breed', default_text=breed, size=(30, 1))],
        [sg.Text('Owner', size=(16, 1)), sg.Input(key='owner', default_text=owner, size=(30, 1))],
        [sg.Text('Date Joined', size=(16, 1)),
         sg.Input(key='date_joined', default_text=date_joined, disabled=True, size=(20, 1)),
         sg.CalendarButton(target='date_joined', button_text='Select', format="%d/%m/%Y", size=(6, 1))],
        [sg.Text('Balance', size=(16, 1)), sg.Input(key='balance', default_text=balance, size=(30, 1), disabled=True)],
        ]

    if mode == 'new':
        dog_edit_layout += [[sg.Exit(), sg.Button('Add')]]
    elif mode == 'edit':
        dog_edit_layout += [[sg.Button('Back'), sg.Save(), sg.Button('Add Payment')]]

    dog_edit_window = sg.Window('New/Edit Dog', dog_edit_layout)

    while True:
        event, values = dog_edit_window.Read()
        if event in (None, 'Back'):
            break
        elif event == 'Add':
            id_ = new_dog(values)
            if id_:
                break
        elif event == 'Save':
            if update_dog(dog, values):
                break
        elif event == 'Add Payment':
            new_balance = add_payment(dog)
            if new_balance:
                dog_edit_window['balance'].Update(new_balance)

    dog_edit_window.close()
    if mode == 'new':
        return id_
    elif mode == 'edit':
        return values['name'], values['owner'], values['breed']


def add_payment(dog):
    while True:
        value = sg.PopupGetText('How much is being added?')
        if value is None:
            return False
        new_balance = dog.add_payment(value)
        if new_balance is False:
            sg.Popup('Please enter a valid amount')
        else:
            return new_balance


def generate_id(name):
    success = False
    while success is False:
        for i in range(0, 100):
            id_ = f'{name[:4].upper()}{i:04d}'
            if id_ not in dogs:
                success = True
                break

        if not success:  # Do more id generation?
            raise ValueError('Can\'t assign ID')

    return id_


def is_valid_date(date):
    return True  # TODO set a proper regex


def new_dog(values):
    global dogs
    name = values['name']
    breed = values['breed']
    owner = values['owner']
    date_joined = values['date_joined']

    # Testing
    if test_dog_input(name, breed, owner, date_joined) is False:
        return False

    id_ = generate_id(name)

    # Add the dog to the list
    dogs[id_] = Dog(id_=id_, name=name, breed=breed, owner=owner, date_joined=date_joined)

    return id_  # if successful


def update_dog(dog, values):
    name = values['name']
    breed = values['breed']
    owner = values['owner']
    date_joined = values['date_joined']

    # Testing
    if test_dog_input(name, breed, owner, date_joined) is False:
        return False

    dog.name = name
    dog.breed = breed
    dog.owner = owner
    dog.date_joined = date_joined

    return True


def test_dog_input(name, breed, owner, date_joined):
    if name == '':
        sg.Popup('Please enter a name')
        return False
    if breed == '':
        sg.Popup('Please enter a breed')
        return False
    if owner == '':
        sg.Popup('Please enter an owner')
        return False
    if date_joined == '':
        sg.Popup('Please select a join date')
        return False
    if is_valid_date(date_joined) is False:
        sg.Popup('The join date is not a valid date')
        return False
    return True


if __name__ == "__main__":
    main_screen()

