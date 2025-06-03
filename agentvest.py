from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

class ROIForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        self.inputs = {}

        fields = [
            ("Purchase Price", "purchase_price"),
            ("Down Payment", "down_payment"),
            ("Loan Interest Rate (%)", "interest_rate"),
            ("Loan Term (Years)", "loan_term"),
            ("Monthly Rent", "monthly_rent"),
            ("Monthly Expenses (Total)", "monthly_expenses")
            ("Property Taxes (Monthly)", "taxes"),
            ("Insurance (Monthly)", "insurance"),
            ("HOA Fees (Monthly)", "hoa"),
            ("Maintenance (Monthly)", "maintenance"),
            ("Property Management (%)", "management_percent"),
            ("Vacancy Rate (%)", "vacancy_percent")
        ]

        for label_text, key in fields:
            self.add_widget(Label(text=label_text))
            input_box = TextInput(multiline=False, input_filter='float')
            self.inputs[key] = input_box
            self.add_widget(input_box)

        calc_btn = Button(text="Calculate ROI", size_hint=(1, 0.3))
        calc_btn.bind(on_press=self.calculate_roi)
        self.add_widget(calc_btn)

        self.result_label = Label(text="")
        self.add_widget(self.result_label)

    def calculate_roi(self, instance):
        try:
            # Base Inputs
            purchase_price = float(self.inputs["purchase_price"].text)
            down_payment = float(self.inputs["down_payment"].text)
            interest_rate = float(self.inputs["interest_rate"].text) / 100 / 12
            loan_term = int(self.inputs["loan_term"].text) * 12
            monthly_rent = float(self.inputs["monthly_rent"].text)
            monthly_expenses = float(self.inputs["monthly_expenses"].text)

            # Expense Inputs
            taxes = float(self.inputs["taxes"].text)
            insurance = float(self.inputs["insurance"].text)
            hoa = float(self.inputs["hoa"].text)
            maintenance = float(self.inputs["maintenance"].text)
            management_percent = float(self.inputs["management_percent"].text) / 100
            vacancy_percent = float(self.inputs["vacancy_percent"].text) / 100

            # Loan Calculation
            loan_amount = purchase_price - down_payment
            mortgage_payment = loan_amount * (interest_rate * (1 + interest_rate) ** loan_term) / ((1 + interest_rate) ** loan_term - 1)

            # Management and vacancy cost (based on rent)
            property_management = monthly_rent * management_percent
            vacancy = monthly_rent * vacancy_percent

            total_monthly_expenses = mortgage_payment + monthly_expenses
            monthly_cash_flow = monthly_rent - total_monthly_expenses
            annual_cash_flow = monthly_cash_flow * 12
            cash_on_cash_roi = (annual_cash_flow / down_payment) * 100

            result = f"Monthly Cash Flow: ${monthly_cash_flow:.2f}\n"
            result += f"Annual Cash Flow: ${annual_cash_flow:.2f}\n"
            result += f"Cash-on-Cash ROI: {cash_on_cash_roi:.2f}%"
            
            self.result_label.text = result

        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"


class AgentVestApp(App):
    def build(self):
        Window.title = "AgentVest"
        return ROIForm()


if __name__ == "__main__":
    AgentVestApp().run()