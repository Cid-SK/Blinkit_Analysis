import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

# Reading the dataset
data_frame = pd.read_csv("Blinkit_cleaned_dataset.csv")

# Streamlit setup
st.set_page_config(page_title="Blinkit Sales Analysis", layout="wide")
st.title(":green[Blinkit] Sales Analysis")

# Sidebar menu
with st.sidebar:
    selected_menu = option_menu("Menu", ["Home", "Analysis", "About"],
                                 icons=['house', 'activity', 'info-circle-fill'],
                                 menu_icon="cast", default_index=1)

# Home tab
if selected_menu == "Home":
    st.divider()
    # Company Overview
    st.subheader(":blue[Company Overview]")
    st.write(
        "Founded in December 2013, Blinkit is leading the charge in transforming India’s vast unorganised grocery landscape through cutting-edge technology and innovation. "
        "We believe every Indian deserves the opportunity to continually improve their life – a process that often begins at home. As part of our mission of helping consumers make healthier, better choices when buying everyday products, "
        "we make a wide range of high-quality grocery and household products available right at their doorsteps within minutes.\n\n"
        "Built on a proprietary technology stack, the Blinkit platform serves as a convergence of consumers looking for everyday essentials, partner stores who serve their needs efficiently, and manufacturers looking for a channel to reach a nation of consumers. "
        "While our technology caters to the burgeoning population of urban India, it is ready and poised to serve the next 100+ million Indians who are yet to start shopping online."
    )

    st.divider()

    st.subheader(":blue[Analysis Overview]")
    # Overview
    st.write("### Overview:")
    st.write("""
    - **Key Metrics:** Displays total sales, average sales, average rating, number of unique items, and total outlets using metrics.
    - **Sales by Item Type:** Visualizes sales distribution through a pie chart, showing the highest and lowest sales item types with key insights.
    - **Sales by Outlet Type:** Another pie chart that presents total sales by outlet type along with insights.
    - **Sales by Outlet Location Type:** A horizontal bar chart showing sales by outlet location type, complemented by insights.
    - **Item Visibility Analysis:** Displays average item visibility by item type using a bar chart.
    """)

    # Fat-Based Analysis
    st.write("### Fat-Based Analysis:")
    st.write("""
    - **Metric Selector:** Users can choose between visualizing total sales or average sales.
    - **Fat Content Sales:** A pie chart shows sales distribution by item fat content with corresponding insights.
    - **Sales by Outlet Location Type and Fat Content:** A bar chart displays sales broken down by outlet location and fat content.
    - **Item Type Sales:** A horizontal bar chart visualizes sales by item type.
    """)

    # Outlet-Based Analysis
    st.write("### Outlet-Based Analysis:")
    st.write("""
    - **Sales by Outlet Establishment Year:** A smooth line chart illustrates sales trends over the years, with insights into total sales, latest year sales, and growth rate.
    - **Sales by Outlet Location Type:** A bar chart presents sales data, along with insights about the highest and lowest sales outlet types.
    - **Sales by Outlet Size:** A donut chart visualizes sales by outlet size, supplemented by key insights.
    - **Outlet Metrics Table:** Displays a comprehensive table summarizing metrics for different outlet types, including total sales, number of items, average sales, average rating, and average item visibility.
    """)
    st.divider()

# Analysis tab
elif selected_menu == "Analysis":
    overview_tab, fat_analysis_tab, outlet_analysis_tab = st.tabs(["**Overview**", "**Fat Based Analysis**", "**Outlet Based Analysis**"])

    # Overview Tab
    with overview_tab:
        # Key Metrics
        total_sales_amount = data_frame['Sales'].sum()
        average_sales_amount = data_frame['Sales'].mean()
        average_rating_value = data_frame['Rating'].mean()
        unique_items_count = data_frame['Item Identifier'].nunique()
        unique_outlets_count = data_frame['Outlet Identifier'].nunique()

        # Display metrics in columns
        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
        col1.metric(":blue[Total Sales]", f"${total_sales_amount:,.2f}")
        col2.metric(":blue[Avg Sales]", f"${average_sales_amount:,.2f}")
        col3.metric(":blue[Average Rating]", f"{average_rating_value:.1f}")
        col4.metric(":blue[Number of Items]", unique_items_count)
        col5.metric(":blue[Total Outlets]", unique_outlets_count)

        st.divider()

        # Sales by Item Type Pie Chart
        st.subheader("Sales by Item Type")

        # Grouping data by Item Type and calculating total sales and item count
        item_sales_data = data_frame.groupby('Item Type').agg({'Sales': 'sum', 'Item Identifier': 'count'}).reset_index()
        item_sales_data.rename(columns={'Item Identifier': 'Item Count'}, inplace=True)

        # Calculate percentage of total sales
        item_sales_data['Percentage'] = (item_sales_data['Sales'] / total_sales_amount) * 100

        # Highest and lowest sales item types
        highest_sales_item = item_sales_data.loc[item_sales_data['Percentage'].idxmax()]
        lowest_sales_item = item_sales_data.loc[item_sales_data['Percentage'].idxmin()]

        total_item_types_count = item_sales_data['Item Type'].nunique()

        col1, col2 = st.columns([2, 1])
        with col1:
            # Creating the pie chart
            pie_chart_item_sales = px.pie(item_sales_data, values='Sales', names='Item Type',
                                           title='Sales Distribution by Item Type',
                                           color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(pie_chart_item_sales)

        with col2:
            # Highlighting key insights
            st.markdown(f"**Out of {total_item_types_count} Total Types**")
            st.markdown(f"**:green[Highest Sales Type:]** {highest_sales_item['Item Type']}")
            st.markdown(f"**:green[Sales Amount:]** ${highest_sales_item['Sales']:,.2f}")
            st.markdown(f"**:green[Percentage of Total Sales:]** {highest_sales_item['Percentage']:.2f}%")
            st.divider()
            st.markdown(f"**:orange[Lowest Sales Type:]** {lowest_sales_item['Item Type']}")
            st.markdown(f"**:orange[Sales Amount:]** ${lowest_sales_item['Sales']:,.2f}")
            st.markdown(f"**:orange[Percentage of Total Sales:]** {lowest_sales_item['Percentage']:.2f}%")

        st.divider()


        # Total Sales by Outlet Type (Pie Chart)
        col1, col2 = st.columns([2, 1])  
        with col1:
            total_sales_by_outlet = data_frame.groupby('Outlet Type')['Sales'].sum().reset_index()
            pie_chart_total_sales = px.pie(total_sales_by_outlet, values='Sales', names='Outlet Type',
                                        title="Total Sales by Outlet Type",
                                        color_discrete_sequence=px.colors.sequential.RdBu, hole=0.7)
            st.plotly_chart(pie_chart_total_sales)
        with col2:
            total_sales = total_sales_by_outlet['Sales'].sum()
            highest_sales_outlet = total_sales_by_outlet.loc[total_sales_by_outlet['Sales'].idxmax()]
            lowest_sales_outlet = total_sales_by_outlet.loc[total_sales_by_outlet['Sales'].idxmin()]

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**Total Sales:** ${total_sales:,.2f}")
            st.markdown(f"**:green[Highest Sales Outlet Type:]** {highest_sales_outlet['Outlet Type']} - ${highest_sales_outlet['Sales']:,.2f}")
            st.markdown(f"**:orange[Lowest Sales Outlet Type:]** {lowest_sales_outlet['Outlet Type']} - ${lowest_sales_outlet['Sales']:,.2f}")

        st.divider()

        # Sales by Outlet Location Type (Horizontal Bar Chart)
        col1, col2 = st.columns([2, 1])
        with col1:
            sales_by_location_type = data_frame.groupby('Outlet Location Type')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=True)
            bar_chart_sales_by_location = px.bar(sales_by_location_type, x='Sales', y='Outlet Location Type', orientation='h',
                                                title="Sales by Outlet Location Type", color='Sales',
                                                color_continuous_scale='greens')
            st.plotly_chart(bar_chart_sales_by_location)
        with col2:
            highest_sales_location = sales_by_location_type.loc[sales_by_location_type['Sales'].idxmax()]
            lowest_sales_location = sales_by_location_type.loc[sales_by_location_type['Sales'].idxmin()]

            # Displaying key insights
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**:green[Highest Sales Location:]** {highest_sales_location['Outlet Location Type']} - ${highest_sales_location['Sales']:,.2f}")
            st.markdown(f"**:orange[Lowest Sales Location:]** {lowest_sales_location['Outlet Location Type']} - ${lowest_sales_location['Sales']:,.2f}")

        st.divider()

        # Item Visibility by Item Type (Bar Chart)
        col1, col2 = st.columns([2, 1])
        with col1:
            # Calculate the average visibility for each item type
            avg_visibility_by_item_type = data_frame.groupby('Item Type')['Item Visibility'].mean().reset_index()
            avg_visibility_by_item_type = avg_visibility_by_item_type.sort_values(by='Item Visibility')

            # Creating the bar chart
            bar_chart_visibility = px.bar(avg_visibility_by_item_type, 
                                        x='Item Visibility', 
                                        y='Item Type', 
                                        orientation='h',
                                        title="Average Item Visibility by Item Type", 
                                        color='Item Visibility',
                                        color_continuous_scale='ylgn')  # Using a color scale
            st.plotly_chart(bar_chart_visibility)

        with col2:
            highest_avg_visibility_type = avg_visibility_by_item_type.loc[avg_visibility_by_item_type['Item Visibility'].idxmax()]
            lowest_avg_visibility_type = avg_visibility_by_item_type.loc[avg_visibility_by_item_type['Item Visibility'].idxmin()]

            # Displaying key insights
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**:green[Highest Average Visibility Item Type:]** {highest_avg_visibility_type['Item Type']} - {highest_avg_visibility_type['Item Visibility']:.2f}")
            st.markdown(f"**:orange[Lowest Average Visibility Item Type:]** {lowest_avg_visibility_type['Item Type']} - {lowest_avg_visibility_type['Item Visibility']:.2f}")

        st.divider()

    # Fat-Based Analysis Tab
    with fat_analysis_tab:
        st.header("Fat Based Analysis")

        # Metric Selector
        selected_metric = st.selectbox("Select Metric to Visualize:", ["Total Sales", "Average Sales"])
        st.divider()
        # Calculate Sales Based on Selected Metric
        if selected_metric == "Total Sales":
            fat_content_sales_data = data_frame.groupby('Item Fat Content')['Sales'].sum().reset_index()
            sales_by_outlet_and_fat_data = data_frame.groupby(['Outlet Location Type', 'Item Fat Content'])['Sales'].sum().reset_index()
            sales_by_item_type_data = data_frame.groupby('Item Type')['Sales'].sum().reset_index().sort_values(by='Sales', ascending=True)
        else:  # Average Sales
            fat_content_sales_data = data_frame.groupby('Item Fat Content')['Sales'].mean().reset_index()
            sales_by_outlet_and_fat_data = data_frame.groupby(['Outlet Location Type', 'Item Fat Content'])['Sales'].mean().reset_index()
            sales_by_item_type_data = data_frame.groupby('Item Type')['Sales'].mean().reset_index().sort_values(by='Sales', ascending=True)

        # Define color palette
        custom_color_palette = ['#CDA900', '#568949']  # Yellow and Green

        # Fat Content Sales Pie Chart
        col1, col2 = st.columns([2, 1])  # Create two columns for the pie chart and insights
        with col1:
            pie_chart_fat_sales = px.pie(fat_content_sales_data, values='Sales', names='Item Fat Content',
                                        title=f"{selected_metric} Distribution by Item Fat Content",
                                        color_discrete_sequence=custom_color_palette, hole=0.7)
            st.plotly_chart(pie_chart_fat_sales)
        with col2:
            total_fat_sales = fat_content_sales_data['Sales'].sum()
            highest_fat_sales = fat_content_sales_data.loc[fat_content_sales_data['Sales'].idxmax()]
            lowest_fat_sales = fat_content_sales_data.loc[fat_content_sales_data['Sales'].idxmin()]

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**Total Sales by Fat Content:** ${total_fat_sales:,.2f}")
            st.markdown(f"**:green[Highest Fat Content Sales:]** {highest_fat_sales['Item Fat Content']} - ${highest_fat_sales['Sales']:,.2f}")
            st.markdown(f"**:orange[Lowest Fat Content Sales:]** {lowest_fat_sales['Item Fat Content']} - ${lowest_fat_sales['Sales']:,.2f}")

        st.divider()

        # Fat Content by Outlet Location Type Bar Chart
        col1, col2 = st.columns([2, 1])  
        with col1:
            bar_chart_fat_outlet = px.bar(sales_by_outlet_and_fat_data, x='Sales', y='Outlet Location Type',
                                        color='Item Fat Content', barmode='group', orientation='h',
                                        title=f"{selected_metric} by Outlet Location Type and Fat Content",
                                        color_discrete_sequence=custom_color_palette)
            st.plotly_chart(bar_chart_fat_outlet)
        with col2:
            highest_outlet_fat_sales = sales_by_outlet_and_fat_data.loc[sales_by_outlet_and_fat_data['Sales'].idxmax()]
            lowest_outlet_fat_sales = sales_by_outlet_and_fat_data.loc[sales_by_outlet_and_fat_data['Sales'].idxmin()]

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**:green[Highest Outlet Sales for Fat Content:]** {highest_outlet_fat_sales['Outlet Location Type']} - ${highest_outlet_fat_sales['Sales']:,.2f}")
            st.markdown(f"**:orange[Lowest Outlet Sales for Fat Content:]** {lowest_outlet_fat_sales['Outlet Location Type']} - ${lowest_outlet_fat_sales['Sales']:,.2f}")

        st.divider()

        # Item Type Horizontal Bar Chart
        bar_chart_item_sales = px.bar(sales_by_item_type_data, x='Sales', y='Item Type', orientation='h',
                                    title=f"{selected_metric} by Item Type", color='Sales',color_continuous_scale='ylgn',
                                    height=600)
        
        st.plotly_chart(bar_chart_item_sales)
        st.divider()

    # Outlet-Based Analysis Tab
    with outlet_analysis_tab:
        st.header("Outlet-Based Analysis")

        st.divider()

        # Sales by Outlet Establishment Year
        sales_by_year_data = data_frame.groupby('Outlet Establishment Year')['Sales'].sum().reset_index()

        # Creating a smooth line chart with filled area
        line_chart_sales_by_year = px.line(sales_by_year_data,
                                            x='Outlet Establishment Year',
                                            y='Sales',
                                            title='Sales by Outlet Establishment Year',
                                            line_shape='spline',  # Makes the line smooth
                                            markers=True)         # Adds markers for each data point

        # Update the trace to have white line and markers with darker yellow filled area
        line_chart_sales_by_year.update_traces(
            line=dict(color='white'),         # Line color white
            marker=dict(color='white'),       # Marker color white
            fill='tozeroy',                   # Fills the area from the line to the x-axis
            fillcolor='rgba(255, 204, 0, 0.8)'  # Darker yellow with less transparency
        )

        # Show the plot
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(line_chart_sales_by_year)
        with col2:
            # Key insights for the line chart
            total_sales_by_year = sales_by_year_data['Sales'].sum()
            latest_year_sales = sales_by_year_data.iloc[-1]['Sales']
            growth_rate = ((latest_year_sales - sales_by_year_data.iloc[0]['Sales']) / sales_by_year_data.iloc[0]['Sales']) * 100

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**Total Sales:** ${total_sales_by_year:,.2f}")
            st.markdown(f"**:orange[Sales in Latest Year:]** ${latest_year_sales:,.2f}")
            st.markdown(f"**:green[Growth Rate:]** {growth_rate:.2f}%")

        st.divider()

        # Sales by Outlet Location Type
        outlet_location_sales_data = data_frame.groupby('Outlet Location Type')['Sales'].sum().reset_index()

        # Custom colors
        custom_color_palette_outlet = ['#FFD700', '#FFFFE0', '#568949']

        bar_chart_outlet_location = px.bar(outlet_location_sales_data,
                                            x='Outlet Location Type',
                                            y='Sales',
                                            title="Sales by Outlet Location Type",
                                            color='Outlet Location Type',
                                            color_discrete_sequence=custom_color_palette_outlet)

        col1, col2 = st.columns([2, 1]) 
        with col1:
            st.plotly_chart(bar_chart_outlet_location)
        with col2:
            # Key insights for the bar chart
            highest_sales_outlet = outlet_location_sales_data.loc[outlet_location_sales_data['Sales'].idxmax()]
            lowest_sales_outlet = outlet_location_sales_data.loc[outlet_location_sales_data['Sales'].idxmin()]

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**:green[Highest Sales Outlet Type:]** {highest_sales_outlet['Outlet Location Type']} - ${highest_sales_outlet['Sales']:,.2f}")
            st.markdown(f"**:orange[Lowest Sales Outlet Type:]** {lowest_sales_outlet['Outlet Location Type']} - ${lowest_sales_outlet['Sales']:,.2f}")

        st.divider()

        # Sales by Outlet Size (Donut Chart)
        outlet_size_sales_data = data_frame.groupby('Outlet Size')['Sales'].sum().reset_index()

        # Creating a donut chart
        donut_chart_outlet_size = px.pie(outlet_size_sales_data,
                                        values='Sales',
                                        names='Outlet Size',
                                        title="Sales by Outlet Size",
                                        hole=0.7,
                                        color_discrete_sequence=custom_color_palette_outlet)

        col1, col2 = st.columns([2, 1])  # Create two columns
        with col1:
            st.plotly_chart(donut_chart_outlet_size)
        with col2:
            # Key insights for the donut chart
            total_sales_by_size = outlet_size_sales_data['Sales'].sum()
            sales_by_high = outlet_size_sales_data.loc[outlet_size_sales_data['Outlet Size'] == 'High', 'Sales'].values[0] if 'High' in outlet_size_sales_data['Outlet Size'].values else 0
            sales_by_small = outlet_size_sales_data.loc[outlet_size_sales_data['Outlet Size'] == 'Small', 'Sales'].values[0] if 'Small' in outlet_size_sales_data['Outlet Size'].values else 0
            sales_by_medium = outlet_size_sales_data.loc[outlet_size_sales_data['Outlet Size'] == 'Medium', 'Sales'].values[0] if 'Medium' in outlet_size_sales_data['Outlet Size'].values else 0
        
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.subheader(":blue[Key Insights]")
            st.markdown(f"**Sales by High Outlets:** ${sales_by_high:,.2f}")
            st.markdown(f"**Sales by Small Outlets:** ${sales_by_small:,.2f}")
            st.markdown(f"**Sales by Medium Outlets:** ${sales_by_medium:,.2f}")

        st.divider()

        # Grouping data by 'Outlet Type' and calculating the required metrics
        outlet_metrics_data = data_frame.groupby('Outlet Type').agg(
            Total_Sales=('Sales', 'sum'),
            Number_of_Items=('Item Identifier', 'nunique'),
            Average_Sales=('Sales', 'mean'),
            Average_Rating=('Rating', 'mean'),
            Average_Item_Visibility=('Item Visibility', 'mean')
        ).reset_index()

        # Rename columns for better readability
        outlet_metrics_data.columns = ['Outlet Type', 'Total Sales', 'No. of Items', 'Avg Sales', 'Avg Rating', 'Avg Item Visibility']

        # Display the metrics table in Streamlit
        st.subheader("Outlet Type Metrics Table")
        st.dataframe(outlet_metrics_data.style.format({
            'Total Sales': '${:,.2f}',  # Format as currency with 2 decimal places
            'Avg Sales': '${:,.2f}',    # Format as currency with 2 decimal places
            'Avg Rating': '{:.2f}',     # Format as rating with 2 decimal places
            'Avg Item Visibility': '{:.2f}'  # Format item visibility with 2 decimal places
        }))

        st.divider()

elif selected_menu == "About":
    st.divider()
    st.subheader(":blue[About Blinkit Sales Analysis App]")
    st.write(
        "This application provides an in-depth analysis of Blinkit's sales data, leveraging powerful visualizations to uncover insights and trends."
    )

    # Interactive Features
    st.subheader(":blue[Interactive Features]")
    st.write("""
    - **Slicers and Selectors:** Users can interactively choose metrics for visualization.
    - **Dynamic Charts:** The app dynamically updates visualizations based on user selections.
    """)

    # Design Elements
    st.subheader(":blue[Design Elements]")
    st.write("""
    - **Visual Appeal:** The app utilizes Plotly for interactive charts, making data visualization engaging.
    - **User-Friendly Layout:** The layout is organized for easy navigation, with clear labels and insights.
    """)

    st.subheader(":blue[Power BI Dashboard]")
    st.write(
        "In addition to this Streamlit app, a detailed Power BI dashboard has been created to visualize and analyze the sales data more interactively. "
        "The dashboard includes various metrics and key performance indicators that help in understanding the sales dynamics at Blinkit."
    )

    # Path to the Power BI dashboard image
    st.image("S:/projects/Blinkit/Blinkit_PowerBi_Dashboard.png", caption="Power BI Dashboard Overview")
