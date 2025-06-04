from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

class ROIForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.inputs = {}

        fields = [
            ("Purchase Price", "purchase_price"),
            ("Down Payment", "down_payment"),
            ("Loan Interest Rate (%)", "interest_rate"),
            ("Loan Term (Years)", "loan_term"),
            ("Monthly Rent", "monthly_rent"),
            ("Expenses (Taxes, Insurance, HOA, Maintenance, etc.)", "total_expenses"),
        ]

        for label_text, key in fields:
            label = Label(text=label_text, size_hint_y=None, height=30)
            input_box = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=40)
            self.inputs[key] = input_box
            self.add_widget(label)
            self.add_widget(input_box)

        calc_btn = Button(text="Calculate ROI", size_hint_y=None, height=50)
        calc_btn.bind(on_press=self.calculate_roi)
        self.add_widget(calc_btn)

        self.result_label = Label(text="", size_hint_y=None, height=120)
        self.add_widget(self.result_label)

    def calculate_roi(self, instance):
        try:
            purchase_price = float(self.inputs["purchase_price"].text)
            down_payment = float(self.inputs["down_payment"].text)
            interest_rate = float(self.inputs["interest_rate"].text) / 100 / 12
            loan_term = int(self.inputs["loan_term"].text) * 12
            monthly_rent = float(self.inputs["monthly_rent"].text)
            total_expenses = float(self.inputs["total_expenses"].text)

            loan_amount = purchase_price - down_payment
            mortgage_payment = loan_amount * (interest_rate * (1 + interest_rate) ** loan_term) / ((1 + interest_rate) ** loan_term - 1)

            total_monthly_expenses = mortgage_payment + total_expenses
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
        scroll = ScrollView()
        form = ROIForm()
        scroll.add_widget(form)
        return scroll

if __name__ == "__main__":
    AgentVestApp().run()


