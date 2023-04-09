# Hall Management System
(CS29202) Software Engineering Lab Project
Created a multi-user hall management system including features such as:
 - Admitting new student accounts into the system, along with the automated allocation of rooms.
 - Allowing mess managers to update mess dues in student accounts.
 - Wardens can view hall occupancy, generate monthly salary reports of mess workers, and view hall accounts. They can also view complaints and file ATRs (Action Taken Reports) addressing them
 -  Hall Clerks can add new temporary employees and their leaves. They can also add petty hall dues.
 - The HMC Chairman can view the total occupancy of halls and generate a monthly mess report for mess managers.
 - Students can view their passbooks, pay fees, and file complaints.
## Installation and Setup
1. Install all dependencies using `pip install -r requirements.txt.`
2. After installing dependencies, run the following commands:
	- `python manage.py makemigrations`
	 - `python manage.py migrate`
	 - `python manage.py runserver`
3. The server should now be running on localhost:8000
4. To login to the admin page, create a superuser using the command:
	`python manage.py createsuperuser`
  
	During creation, set the role to `admin`.

To be able to make payments using Stripe:
1. Replace `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` in `settings.py` with your own keys that you can generate from [Stripe](https://stripe.com/).
2. Open a terminal and run the commands:
   - `./stripe login`
   - `STRIPE_SECRET_KEY="INSERT YOUR STRIPE SECRET KEY HERE"`
   - `./stripe listen --forward-to http://localhost:8000/passbook/pay/stripe_webhook --api-key $STRIPE_SECRET_KEY`
