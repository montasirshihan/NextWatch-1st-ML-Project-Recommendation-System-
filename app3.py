import streamlit as st ##for building the UI of the website
import pickle
import pandas as pd

# 1. Load the data
maindf_dict=pickle.load(open('main_df.pkl', 'rb'))

maindf=pd.DataFrame(maindf_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))



#no 2: the recommendation function

def recommendationSystem(content,selected_filters):

    if content in maindf['title'].values:

        content_index = maindf[maindf['title']==content].index[0]
    
    else:
        print("Content not found in database.")
        return []
        
    
    distances=similarity[content_index]

    Suggestions=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:50]
    
    recommend_Contents=[]
  

    for i in Suggestions:
    # i[0] is the index of the recommended content in maindf
        row= maindf.iloc[i[0]]

        # FILTER LOGIC: Only add if the content_type is in the user's list
        if row.content_type in selected_filters:
            recommend_Contents.append({
            'title':row.title,
            'id': row.id,
            'type': row.content_type

        })
        
        
        if len(recommend_Contents)==10 :
            break

    return recommend_Contents


# 3. now Build the Website UI

st.set_page_config(page_title="Welcome NextWatch!! Recommender System", layout="wide")

st.title('NextWatch!! Recommender System')
st.markdown("### Find your next favorite Movie, Anime, or TV Shows according to your Taste!!")

##set sidebar for Filtering Option
st.sidebar.header("Filter Results")
all_types =maindf['content_type'].unique()
selected_filters =st.sidebar.multiselect(
    "Show only:",
    options=all_types,
    default=list(all_types) # Shows everything by default
)

selected_Contentname= st.selectbox(
    'Which Anime/Movie/TvShows do you like?',
    maindf['title'].values
)

if st.button('Recommend'):
    recommendations=recommendationSystem(selected_Contentname,selected_filters)

    st.subheader(f"Recommendations for {selected_Contentname}:")

    if not recommendations:
        st.warning("No matches found for those filters. Try selecting more options in the sidebar.")
    else:

        for i, item in enumerate(recommendations, start=1):
       # Build the correct TMDB URL based on content type
            if item['type']=='Movie':
             url= f"https://www.themoviedb.org/movie/{item['id']}"
             tag_color = "orange"

            else:
             url = f"https://www.themoviedb.org/tv/{item['id']}"
             tag_color = "blue"

             # This container acts as your "Box"
            with st.container(border=True): 
                col1, col2 = st.columns([0.8, 0.2])
                
                with col1:
                    st.markdown(f"### {i}. [{item['title']}]({url})")
                    st.caption(f"Type: {item['type']}")
                
                with col2:
                    # A small visual indicator for the type
                    st.markdown(f":{tag_color}[● {item['type']}]")


        



           

    