from reactpy import component, html, run


@component
def App():
    return html.div(
        html.h1("Myself"),
        html.p("Name: Nethum Perera"),
        html.p("Age: 22"),
        html.p("NIC: 200125902901"),
        html.p("Address: 139/3, Suhada Mw, Katuwawala, Boralesgamuwa, 10290"),
        html.p("High School: Royal College, Colombo 07"),
        html.p("Academic Higher Qualifications: "),
    )

run(App)
