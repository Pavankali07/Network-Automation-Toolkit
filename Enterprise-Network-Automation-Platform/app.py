from flask import Flask, render_template, request
from network_automation.services import NetworkService

app = Flask(__name__)
service = NetworkService()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", devices=service.inventory())

@app.route("/report/<name>")
def report(name):
    actions = {
        "inventory": service.inventory,
        "backup": service.backup,
        "compliance": service.compliance,
        "interfaces": service.interfaces,
        "bgp": service.bgp,
        "ospf": service.ospf,
        "drift": service.drift,
    }
    return render_template("report.html", title=name.title(), results=actions[name]())

@app.route("/vlan", methods=["GET", "POST"])
def vlan():
    if request.method == "POST":
        results = service.vlan(
            int(request.form["vlan_id"]),
            request.form["vlan_name"],
            request.form.getlist("devices"),
        )
        return render_template("report.html", title="VLAN Deployment", results=results)
    return render_template("vlan.html", devices=service.devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
