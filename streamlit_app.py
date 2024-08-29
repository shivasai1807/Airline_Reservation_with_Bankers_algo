import streamlit as st

class Flight:
    def __init__(self, flight_id, economy_seats, business_seats, first_class_seats):
        self.flight_id = flight_id
        self.total_seats = [economy_seats, business_seats, first_class_seats]
        self.available_seats = self.total_seats.copy()
        self.booked_seats = [0, 0, 0]

class Passenger:
    def __init__(self, name, economy_seats, business_seats, first_class_seats):
        self.name = name
        self.seat_request = [economy_seats, business_seats, first_class_seats]

class ReservationSystem:
    def __init__(self):
        self.flights = {}

    def add_flight(self, flight):
        self.flights[flight.flight_id] = flight

    def request_booking(self, flight_id, passenger):
        if flight_id not in self.flights:
            return False, "Flight not found"

        flight = self.flights[flight_id]
        if self.check_safety(flight, passenger.seat_request):
            self.make_booking(flight, passenger.seat_request)
            return True, "Booking successful"
        else:
            return False, "Booking cannot be made at this time"

    def check_safety(self, flight, request):
        return all(flight.available_seats[i] >= request[i] for i in range(3))

    def make_booking(self, flight, request):
        for i in range(3):
            flight.available_seats[i] -= request[i]
            flight.booked_seats[i] += request[i]

    def cancel_booking(self, flight_id, request):
        if flight_id not in self.flights:
            return False, "Flight not found"

        flight = self.flights[flight_id]
        for i in range(3):
            if flight.booked_seats[i] < request[i]:
                return False, "Cannot cancel more seats than booked"
            flight.available_seats[i] += request[i]
            flight.booked_seats[i] -= request[i]
        return True, "Booking cancelled successfully"

    def display_flight_status(self, flight_id):
        if flight_id not in self.flights:
            return None, "Flight not found"
        
        flight = self.flights[flight_id]
        status = (
            f"Economy Seats: {flight.booked_seats[0]}/{flight.total_seats[0]} booked\n"
            f"Business Seats: {flight.booked_seats[1]}/{flight.total_seats[1]} booked\n"
            f"First Class Seats: {flight.booked_seats[2]}/{flight.total_seats[2]} booked"
        )
        return True, status

# Streamlit app
def main():
    st.title("Airline Reservation System")
    
    # Initialize reservation system
    reservation_system = ReservationSystem()
    
    # Adding some sample flights
    if 'initialized' not in st.session_state:
        reservation_system.add_flight(Flight("FL001", 100, 20, 10))
        reservation_system.add_flight(Flight("FL002", 150, 30, 15))
        st.session_state['reservation_system'] = reservation_system
        st.session_state['initialized'] = True
    else:
        reservation_system = st.session_state['reservation_system']
    
    menu = ["Book a Ticket", "Cancel a Booking", "Display Flight Status", "Display Available Flights", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Book a Ticket":
        st.subheader("Book a Ticket")
        flight_id = st.text_input("Enter Flight ID:")
        name = st.text_input("Enter Passenger Name:")
        economy_seats = st.number_input("Number of Economy seats:", min_value=0, step=1)
        business_seats = st.number_input("Number of Business seats:", min_value=0, step=1)
        first_class_seats = st.number_input("Number of First Class seats:", min_value=0, step=1)
        
        if st.button("Book"):
            passenger = Passenger(name, economy_seats, business_seats, first_class_seats)
            success, message = reservation_system.request_booking(flight_id, passenger)
            st.success(message) if success else st.error(message)
    
    elif choice == "Cancel a Booking":
        st.subheader("Cancel a Booking")
        flight_id = st.text_input("Enter Flight ID:")
        economy_seats = st.number_input("Number of Economy seats to cancel:", min_value=0, step=1)
        business_seats = st.number_input("Number of Business seats to cancel:", min_value=0, step=1)
        first_class_seats = st.number_input("Number of First Class seats to cancel:", min_value=0, step=1)
        
        if st.button("Cancel"):
            cancel_request = [economy_seats, business_seats, first_class_seats]
            success, message = reservation_system.cancel_booking(flight_id, cancel_request)
            st.success(message) if success else st.error(message)

    elif choice == "Display Flight Status":
        st.subheader("Display Flight Status")
        flight_id = st.text_input("Enter Flight ID:")
        if st.button("Show Status"):
            success, message = reservation_system.display_flight_status(flight_id)
            st.text(message) if success else st.error(message)
    
    elif choice == "Display Available Flights":
        st.subheader("Available Flights")
        flights = list(reservation_system.flights.keys())
        for flight in flights:
            st.text(flight)
    
    elif choice == "Exit":
        st.write("Thank you for using the Airline Reservation System. Goodbye!")

if __name__ == "__main__":
    main()
