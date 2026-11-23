from flask import Flask, request

app = Flask(__name__)

# Plain HTML string inside Python (no separate HTML file needed)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Basic Payroll Estimator</title>
</head>
<body style="font-family: sans-serif; margin: 40px;">

    <h2>Basic Payroll Tax Estimator (FY 2026-27)</h2>

    <form method="POST">
        <label>Annual CTC (Rs.): </label>
        <input type="number" name="ctc" value="{ctc}" required>
        <button type="submit">Calculate</button>
    </form>

    {table}

</body>
</html>
"""


def calculate_payroll(ctc):
    # 1. Basic = 50% of CTC, Employer PF = 12% of Basic
    basic = ctc * 0.50
    employer_pf = basic * 0.12
    gross = ctc - employer_pf

    # 2. Employee Deductions
    employee_pf = employer_pf
    prof_tax = 2400  # Rs. 200/month

    # 3. Income Tax (New Regime FY 2026-27: Rs. 75,000 standard deduction)
    taxable = max(0, gross - 75000)

    # Zero tax if taxable income is up to Rs. 12,00,000
    if taxable <= 1200000:
        tax = 0
    else:
        tax = 0
        if taxable > 400000:
            tax += min(taxable - 400000, 400000) * 0.05
        if taxable > 800000:
            tax += min(taxable - 800000, 400000) * 0.10
        if taxable > 1200000:
            tax += min(taxable - 1200000, 400000) * 0.15
        if taxable > 1600000:
            tax += min(taxable - 1600000, 400000) * 0.20
        if taxable > 2000000:
            tax += min(taxable - 2000000, 400000) * 0.25
        if taxable > 2400000:
            tax += (taxable - 2400000) * 0.30

        tax = tax * 1.04  # Add 4% cess

    # 4. Net Take-Home
    net_annual = gross - employee_pf - prof_tax - tax
    net_monthly = net_annual / 12

    return round(gross), round(employee_pf), round(prof_tax), round(tax), round(net_annual), round(net_monthly)


@app.route("/", methods=["GET", "POST"])
def home():
    ctc = 1500000
    table = ""

    if request.method == "POST":
        ctc = float(request.form.get("ctc", 0))
        gross, pf, pt, tax, net_annual, net_monthly = calculate_payroll(ctc)

        table = f"""
        <br>
        <table border="1" cellpadding="8" cellspacing="0">
            <tr><th>Item</th><th>Amount (Rs.)</th></tr>
            <tr><td>Annual CTC</td><td>{round(ctc)}</td></tr>
            <tr><td>Gross Salary</td><td>{gross}</td></tr>
            <tr><td>Employee PF</td><td>- {pf}</td></tr>
            <tr><td>Professional Tax</td><td>- {pt}</td></tr>
            <tr><td>Income Tax</td><td>- {tax}</td></tr>
            <tr><td><b>Annual Take-Home</b></td><td><b>{net_annual}</b></td></tr>
            <tr><td><b>Monthly Take-Home</b></td><td><b>{net_monthly}</b></td></tr>
        </table>
        """

    return HTML_PAGE.format(ctc=int(ctc), table=table)


if __name__ == "__main__":
    app.run(debug=True)