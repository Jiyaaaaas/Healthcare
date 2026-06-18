from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HeartPrediction, DiabetesPrediction, MenstrualPrediction

import matplotlib
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
import pandas as pd
import io, base64
from sklearn.ensemble import RandomForestClassifier

# -------------------- DIABETES --------------------
@login_required
def predict_diabetes(request):
    df = pd.read_csv("diabetes.csv")

    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    model = RandomForestClassifier()
    model.fit(X, y)

    result = None
    chart_bar = chart_pie = chart_hist = chart_importance = None

    if request.method == "POST":
        pregnancies = int(request.POST.get("pregnancies", 0))
        glucose = float(request.POST.get("glucose", 0))
        bp = float(request.POST.get("bp", 0))
        skin = float(request.POST.get("skin_thickness", 0))
        insulin = float(request.POST.get("insulin", 0))
        bmi = float(request.POST.get("bmi", 0))
        pedigree = float(request.POST.get("diabetes_pedigree", 0))
        age = float(request.POST.get("age", 0))

        input_data = [[pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age]]

        pred = model.predict(input_data)
        prob = model.predict_proba(input_data)[0][1] * 100

        result = "High Risk" if pred[0] == 1 else "Low Risk"

        DiabetesPrediction.objects.create(
            user=request.user,
            pregnancies=pregnancies,
            glucose=glucose,
            bp=bp,
            skin_thickness=skin,
            insulin=insulin,
            bmi=bmi,
            diabetes_pedigree=pedigree,
            age=age,
            result=result
        )

        # BAR
        fig1, ax1 = plt.subplots()
        ax1.bar(["Glucose","BP","BMI","Age"], [glucose, bp, bmi, age])
        ax1.set_title("Diabetes Inputs")
        buf1 = io.BytesIO()
        fig1.savefig(buf1, format='png')
        chart_bar = base64.b64encode(buf1.getvalue()).decode()
        buf1.close()
        plt.close(fig1)

        # PIE
        fig2, ax2 = plt.subplots()
        ax2.pie([prob, 100-prob], labels=["Risk","Safe"], autopct='%1.1f%%')
        ax2.set_title("Diabetes Risk %")
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format='png')
        chart_pie = base64.b64encode(buf2.getvalue()).decode()
        buf2.close()
        plt.close(fig2)

        # HISTOGRAM
        fig3, ax3 = plt.subplots()
        ax3.hist(df["Glucose"], bins=20)
        ax3.axvline(glucose)
        ax3.set_title("Glucose Comparison")
        buf3 = io.BytesIO()
        fig3.savefig(buf3, format='png')
        chart_hist = base64.b64encode(buf3.getvalue()).decode()
        buf3.close()
        plt.close(fig3)

        # FEATURE IMPORTANCE
        fig4, ax4 = plt.subplots()
        ax4.barh(X.columns, model.feature_importances_)
        ax4.set_title("Feature Importance")
        buf4 = io.BytesIO()
        fig4.savefig(buf4, format='png')
        chart_importance = base64.b64encode(buf4.getvalue()).decode()
        buf4.close()
        plt.close(fig4)

    return render(request, "predict_diabetes.html", {
        "result": result,
        "chart_bar": chart_bar,
        "chart_pie": chart_pie,
        "chart_hist": chart_hist,
        "chart_importance": chart_importance
    })


# -------------------- HEART --------------------
@login_required
def predict_heart(request):
    df = pd.read_csv("heart.csv")

    df["Sex"] = df["Sex"].map({"M": 1, "F": 0})
    df["ChestPainType"] = df["ChestPainType"].map({"TA": 0, "ATA": 1, "NAP": 2, "ASY": 3})
    df["RestingECG"] = df["RestingECG"].map({"Normal": 0, "ST": 1, "LVH": 2})
    df["ExerciseAngina"] = df["ExerciseAngina"].map({"Y": 1, "N": 0})
    df["ST_Slope"] = df["ST_Slope"].map({"Up": 0, "Flat": 1, "Down": 2})

    X = df.drop("HeartDisease", axis=1)
    y = df["HeartDisease"]

    model = RandomForestClassifier()
    model.fit(X, y)

    result = None
    chart_bar = chart_pie = chart_hist = chart_importance = None

    if request.method == "POST":
        age = int(request.POST["age"])
        sex = int(request.POST["sex"])
        chestpain = int(request.POST["chestpain"])
        restingbp = float(request.POST["restingbp"])
        cholesterol = float(request.POST["cholesterol"])
        fastingbs = int(request.POST["fastingbs"])
        maxhr = float(request.POST["maxhr"])
        exerciseangina = int(request.POST["exerciseangina"])
        oldpeak = float(request.POST["oldpeak"])
        st_slope = int(request.POST["st_slope"])
        restingecg = 0

        input_data = [[age, sex, chestpain, restingbp, cholesterol,
                       fastingbs, maxhr, exerciseangina, oldpeak, st_slope, restingecg]]

        pred = model.predict(input_data)
        prob = model.predict_proba(input_data)[0][1] * 100

        result = "High Risk" if pred[0] == 1 else "Low Risk"

        HeartPrediction.objects.create(
            user=request.user,
            age=age,
            sex=sex,
            chestpain=chestpain,
            restingbp=restingbp,
            cholesterol=cholesterol,
            fastingbs=fastingbs,
            maxhr=maxhr,
            exerciseangina=exerciseangina,
            oldpeak=oldpeak,
            st_slope=st_slope,
            result=result
        )

        # BAR
        fig1, ax1 = plt.subplots()
        ax1.bar(["Age","BP","Chol","HR","Oldpeak"],
                [age, restingbp, cholesterol, maxhr, oldpeak])
        ax1.set_title("Heart Input Parameters")
        buf1 = io.BytesIO()
        fig1.savefig(buf1, format='png')
        chart_bar = base64.b64encode(buf1.getvalue()).decode()
        buf1.close()
        plt.close(fig1)

        # PIE
        fig2, ax2 = plt.subplots()
        ax2.pie([prob, 100-prob], labels=["Risk %", "Safe %"], autopct='%1.1f%%')
        ax2.set_title("Heart Risk")
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format='png')
        chart_pie = base64.b64encode(buf2.getvalue()).decode()
        buf2.close()
        plt.close(fig2)

        # HISTOGRAM
        fig3, ax3 = plt.subplots()
        ax3.hist(df["Cholesterol"], bins=20)
        ax3.axvline(cholesterol)
        ax3.set_title("Cholesterol Comparison")
        buf3 = io.BytesIO()
        fig3.savefig(buf3, format='png')
        chart_hist = base64.b64encode(buf3.getvalue()).decode()
        buf3.close()
        plt.close(fig3)

        # FEATURE IMPORTANCE
        fig4, ax4 = plt.subplots()
        ax4.barh(X.columns, model.feature_importances_)
        ax4.set_title("Feature Importance")
        buf4 = io.BytesIO()
        fig4.savefig(buf4, format='png')
        chart_importance = base64.b64encode(buf4.getvalue()).decode()
        buf4.close()
        plt.close(fig4)

    return render(request, "predict_heart.html", {
        "result": result,
        "chart_bar": chart_bar,
        "chart_pie": chart_pie,
        "chart_hist": chart_hist,
        "chart_importance": chart_importance
    })


# -------------------- MENSTRUAL --------------------
@login_required
def predict_menstrual(request):
    result = None
    chart_pie = chart_bar = None

    if request.method == "POST":
        cycle_length = int(request.POST["cycle_length"])
        bleeding_days = int(request.POST["bleeding_days"])
        pain_level = int(request.POST["pain_level"])
        stress = int(request.POST.get("stress", 0))
        sleep = float(request.POST.get("sleep", 0))
        weight_change = float(request.POST.get("weight_change", 0))

        score = 0
        if not (24 <= cycle_length <= 32): score += 1
        if not (3 <= bleeding_days <= 7): score += 1
        if pain_level > 5: score += 1
        if stress > 6: score += 1
        if sleep < 6: score += 1
        if abs(weight_change) > 3: score += 1

        if score >= 3:
            result = "Irregular Cycle"
            risk_percent = 75
        else:
            result = "Normal Cycle"
            risk_percent = 20

        MenstrualPrediction.objects.create(
            user=request.user,
            cycle_length=cycle_length,
            bleeding_days=bleeding_days,
            pain_level=pain_level,
            result=result
        )

        # PIE
        fig1, ax1 = plt.subplots()
        ax1.pie([risk_percent, 100-risk_percent],
                labels=["Risk", "Healthy"], autopct='%1.1f%%')
        ax1.set_title("Cycle Health")
        buf1 = io.BytesIO()
        fig1.savefig(buf1, format='png')
        chart_pie = base64.b64encode(buf1.getvalue()).decode()
        buf1.close()
        plt.close(fig1)

        # BAR
        fig2, ax2 = plt.subplots()
        ax2.bar(["Cycle","Bleeding","Pain","Stress","Sleep"],
                [cycle_length, bleeding_days, pain_level, stress, sleep])
        ax2.set_title("Health Parameters")
        buf2 = io.BytesIO()
        fig2.savefig(buf2, format='png')
        chart_bar = base64.b64encode(buf2.getvalue()).decode()
        buf2.close()
        plt.close(fig2)

    return render(request, "predict_menstrual.html", {
        "result": result,
        "chart_pie": chart_pie,
        "chart_bar": chart_bar
    })


# -------------------- PROFILE --------------------
@login_required
def profile_view(request):
    tab = request.GET.get("tab", "heart")

    return render(request, "profile.html", {
        "tab": tab,
        "heart_predictions": HeartPrediction.objects.filter(user=request.user),
        "diabetes_predictions": DiabetesPrediction.objects.filter(user=request.user),
        "menstrual_predictions": MenstrualPrediction.objects.filter(user=request.user),
    })