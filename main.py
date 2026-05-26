while True:
    print('1. Search Rooms')
    print('2. Create Reservation')
    print('3. Check Out')
    print('4. View Reservation')
    print('5. Access Admin Actions')
    print('6. Exit')

    choice = input('Enter your choice: ')
    if choice == '1':
        break

    if choice == '6':
        print('Thank you. Have a great day.')
        break

    else:
        print('Please select available options (1-6).')
