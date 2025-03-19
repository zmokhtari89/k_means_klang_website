import streamlit as st

# Website Header
st.markdown("""
    <h1 style="text-align: center; color: #ecd4cf;">Music is More Than Just a Genre</h1>
    <br>
""", unsafe_allow_html=True)

#Giphy 
# URL of your Giphy GIF
giphy_url = "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWtoOGdjZzltOTEwczM1YjY5eXJmdTJrM3M0a3M3M2JwMnV1eGw2ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/awiM51Q3K2l4Joe4xS/giphy.gif"

# Display the GIF
st.image(giphy_url, use_column_width=True)

# Section 1 : Our Motivation. Our Why?  
st.markdown('''<br>
            <h2 style="text-align: center;">Our Project Motivation</h2>
            ''',
            unsafe_allow_html=True)
st.markdown('''<p style="text-align: justify; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.2;"> <b>Genres are not well-defined. And they don’t define what we hear.</b>. 
            Sometimes is easy to distinguish between Metal and classical. But what about all the types of sounds inbetween? Can we really confidently say what is Soft-Rock vs Reggae? Hip-hop vs Funk? Blues vs Jazz? 
            Unfortunately, genre labels don't tell us enough about a sound. 
            <br> <br>
            <i>But, luckily, our brains do!</i> When we listen to music our brain registers certain patterns, frequencies, and features that evoke:<br><b><i> Emotions </b></i> 🤗  and <b><i> Memories </b></i> 🥳 
            </p><br>''', unsafe_allow_html=True)
 


# # Provide the image path or URL
# image_path = "path/to/your/image.png"  # can also be a URL

# # Display the image
# st.image(image_path, caption="My Image", use_column_width=True)

#Section 2: Our Approach. simplefied
st.markdown('''<br>
            <h2 style="text-align: center;">Our Approach</h2>
            ''',
            unsafe_allow_html=True)
st.markdown('''<p style="text-align: justify; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.2;"><b>Unsatisfied with the status-quo, we set off to look beyond the label!</b> 🔎 We wanted to see what features are important for describing how particular songs and sounds might make us feel.  
            <br><br>
            <b>Under the hood:</b> Using Data Analytics techniques (Python, Librosa), we took music samples from the GTZAN Dataset(link), stripped it of the predefined genre labels, and broke the samples down into their musical building blocks. Then we used a K-means unsupervised learning algorithm to cluster those sounds based on the relationship between the distinctive features (eg. a sound timbre, harmony, sharpness, brightness, etc). We found that various sound attributes helped to explain how certain sounds clustered together. For example: brightness, is it noisy or focused, is the timbre textured and complex or clean 
            <br><br>
            <b>The fun part</b>: Now we can upload audio files and discover more meaning behind the music. How is it related to the other sounds? What is the personality of the song and what are its characteristics? 
            🛢️Check out our Github here(link) for more details 
            <br><br>
            Give it a try!  Upload your favorite song (or voice sample! 😁) and have fun!
            </p>''', unsafe_allow_html=True)




# #Section 4: The future of music (Discovering the roots of music, )
# st.markdown('''<br>
#             <h2 style="text-align: center;">Future Applications: Understanding the Stories that Music Wants to Tell</h2>
#             <br>
#             <h4 style="text-align: center; ">text here</h4>''',
#             unsafe_allow_html=True)
