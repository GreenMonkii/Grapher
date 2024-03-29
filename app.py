# Importing Libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import math

def _generate_table_of_values(rov, eqn_type: str, *args) -> pd.DataFrame:
    """
        This function takes in a range of values, equation type and positional arguements as its parameters 
        and returns a Pandas Dataframe object.
    """
    match eqn_type.lower():
        # Match statement to carry out various operations based on the value of the **eqn_type** parameter
        case "quad":
            coeff1, coeff2, constant = args[0], args[1], args[2]
            # table_of_values["y"] uses list comprehension to create a list where each of the values in the range are plugged into the function
            table_of_values = dict(y=[(coeff1*(i**2) + coeff2*i + constant)
                                      for i in range(*rov)], x=[i for i in range(*rov)])
        
        case "lin":
            coeff1, constant = args[0], args[1]
            table_of_values = dict(y=[(coeff1*i + constant)
                                      for i in range(*rov)], x=[i for i in range(*rov)])

        case "poly":
            coeffs = args[0]
            x = [i for i in range(*rov)]
            # This is an iterable containing a list of values of the equation applied term by term for each value in the range (rov)
            y_fragments = map(
                lambda i: [j*(i**(len(coeffs)-coeffs.index(j)-1)) for j in coeffs], x)
            table_of_values = dict(y=list(map(sum, y_fragments)), x=x)

        case "trig":
            coeffs = args[0]
            theta = [i for i in range(*rov, 15)]
            # Creating functions that will resolve each of the trigonometric functions e.g the sin function resolves the sine part of the input, etc.
            def sin(x): return coeffs[0]*(math.sin(x))
            def cos(x): return coeffs[1]*(math.cos(x))
            def tan(x): return coeffs[2]*(math.tan(x))

            def sec(x): return coeffs[3]*(1/math.cos(x)
                                          if math.cos(x) != 0 else 1.633123935319537e+16)

            def cosec(x): return coeffs[4]*(1/math.sin(x)
                                            if math.sin(x) != 0 else 1.633123935319537e+16)
            def cot(x): return coeffs[5]*(1/math.tan(x)
                                          if math.tan(x) != 0 else 1.633123935319537e+16)
            y = list(map(lambda x: sum((sin(x), cos(x), tan(x), sec(
                x), cosec(x), cot(x), coeffs[6])), map(math.radians, theta)))
            table_of_values = dict(y=y, x=theta)

    return pd.DataFrame(table_of_values)


def main():
    st.set_page_config("GraphER", r'res/favicon.png')
    st.image(r'res/cover.png',
             caption='GraphER by TL. Python Graphing Application Implemented Using Streamlit, Pandas🐼 and Plotly📉')
    eqn = st.selectbox("Select the Kind of Equation", [
                       "Linear", "Quadratic", "Polynomial", "Trigonometric", "Simultaneous"])
    match eqn:

        case "Linear":
            col1, col2 = st.columns(2)
            with col1:
                coeff1 = st.number_input("$x$", key="key-SWbLr")
            with col2:
                constant = st.number_input("$constant$", key="key-eXocy")
            rov = st.slider("Choose Your Range of Values", -10, 10, (0, 5))
            data = _generate_table_of_values(rov, "lin", coeff1, constant)
            # title = f"Graph of {coeff1 if coeff1 != 1 else ''}x {f'+ {constant}' if constant >= 0 else constant}"
            title = "Graph of the Linear Function"

        case "Quadratic":
            col1, col2, col3 = st.columns(3)
            with col1:
                coeff1 = st.number_input("$x^2$", key="key-qXVli")
            with col2:
                coeff2 = st.number_input("$x$", key="key-vJqYV")
            with col3:
                constant = st.number_input("$constant$", key="key-rNjTK")
            rov = st.slider("Choose Your Range of Values", -10, 10, (0, 5))
            data = _generate_table_of_values(
                rov, "quad", coeff1, coeff2, constant)

            # title = f"Graph of {coeff1 if coeff1 != 1 else ''}x<sup>2</sup> {f'+ {coeff2}' if coeff2 >= 0 else coeff2}x {f'+ {constant}' if constant >= 0 else constant}"
            title = "Graph of the Quadratic Function"

        case "Polynomial":
            terms = st.number_input("Enter the order of the equation", min_value=3,
                                    max_value=10, step=1, help="Input the highest power in the equation")
            coeffs = []
            for index, col in enumerate(st.columns(terms+1)):
                with col:
                    if index != terms:
                        coeff = st.number_input(f"$x^{(terms-index)}$")
                        coeffs.append(coeff)
                    else:
                        constant = st.number_input("$constant$", key="key-$AtHQ")
                        coeffs.append(constant)
            else:
                rov = st.slider("Choose Your Range of Values", -10, 10, (0, 5))
                data = _generate_table_of_values(rov, "poly", coeffs)

            title = "Graph of the Polynomial Function"

        case "Trigonometric":
            st.info("""Input the co-efficient for the trigonometric functions in the input box below them!
                    For example, for $2sinθ$ , we would have $2$ in the box below $sinθ$.
                    Leave out anyone not included in your trigonometric function!
                    """, icon="ℹ️")
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            with col1:
                sin = st.number_input("$sinθ$")
            with col2:
                cos = st.number_input("$cosθ$")
            with col3:
                tan = st.number_input("$tanθ$")
            with col4:
                cosec = st.number_input("$cosecθ$")
            with col5:
                sec = st.number_input("$secθ$")
            with col6:
                cot = st.number_input("$cotθ$")
            with col7:
                constant = st.number_input("$constant$", key="key-CRugi")

            coeffs = (sin, cos, tan, cosec, sec, cot, constant)
            start_range, end_range = st.slider("Choose Your Range of Values", -
                                               360, 360, (0, 180), step=15)
            # Increment the value of the max range value by 1 to make sure that it is inclusive
            rov = (start_range, end_range+1)
            data = _generate_table_of_values(rov, "trig", coeffs)

            title = "Graph of the Trigonometric Function"

        case "Simultaneous":
            st.write("$For Equation 1$")
            col1, col2 = st.columns(2)
            with col1:
                coeff1 = st.number_input("$x$", key="key-DdgQX")
            with col2:
                constant = st.number_input("$constant$", key="key-pJYQF")

            st.write("$For Equation 2$")
            col3, col4 = st.columns(2)
            with col3:
                coeff2 = st.number_input("$x$", key="key-XjRJI")
            with col4:
                _constant = st.number_input("$constant$", key="key-udCGK")
            # rov = st.slider("Choose Your Range of Values", -10, 10, (0, 5))
            rov = st.slider("Choose Your Range of Values", -10, 10, (0, 5))
            df1 = _generate_table_of_values(rov, "lin", coeff1, constant)
            df2 = _generate_table_of_values(rov, "lin", coeff2, _constant)
            df1.rename(columns={"y": "y1"}, inplace=True)
            df2.rename(columns={"y": "y2"}, inplace=True)
            data = pd.concat([df1.set_index('x'), df2.set_index('x')], axis=1)

            title = "Graph of the Simultaneous Linear Functions"

    # color = st.color_picker("Choose the line color for your graph")
    
    # Handling when the 'Generate Graph' button is clicked
    if st.button("Generate Graph", type="primary"):
        st.table(data)
        if eqn != "Simultaneous":
            figure = px.line(data, x="x", y="y", markers=True, title=title)
        else:
            figure = px.line(data, y=["y1", "y2"], markers=True, title=title)

        # st.line_chart(data, x="x", y="y", color="#ff0000")
        figure.update_traces(line=dict(color="#505050"))
        figure.update_layout(
            title=dict(x=0.4, font={"family": "Open Sans", "size": 18}),
            xaxis=dict(
                title="X-axis",
                showline=True,
                zeroline=True,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            yaxis=dict(
                title="Y-axis",
                showline=True,
                zeroline=True,
                showticklabels=True,
                linecolor='rgb(204, 204, 204)',
                linewidth=2,
                ticks='outside',
                tickfont=dict(
                    family='Arial',
                    size=12,
                    color='rgb(82, 82, 82)',
                ),
            ),
            showlegend=False,
            # plot_bgcolor='white'
        )
        st.plotly_chart(figure, theme="streamlit")


if __name__ == "__main__":
    main()
