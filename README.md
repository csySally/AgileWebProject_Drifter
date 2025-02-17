# DRIFTER

## About the Application

In this fast-paced world, everyone's heart harbours unspoken mysteries and late-night musings. Do those unspoken secrets in casual conversations or written silently on the pages of your diary sometimes make you feel lonely and helpless? Have you ever wanted to find an outlet for those questions?

Welcome to "Drifter" - a unique platform for your questions to fly freely in an anonymous world. Here, everyone can be a listener and a sharer. Whether it's late-night blues, dawn doubts, or those flashes of inspiration and things you haven't told others, they can all find their home here.

"Drifter" makes the power of anonymity gentle and powerful. There are no preconceived prejudices, only stories waiting to be discovered and mysteries to be solved. Send a secret note and it will randomly fly to a corner of the world; reply to a stranger's query and your words may become a beacon for them. In the process, different people will gather around a secret or question, sharing their perspectives so that everyone's experience is resonated and understood.

Please speak up at Drifter!

## Deisgn

In "Drifter", our design concept was to create a warm, simple and inclusive platform for anonymous communication. The idea was inspired by some famous dating apps, but our platform is not about making friends, it is about getting different responses to one's thoughts, so that everyone can feel free to speak their mind. Designer <b>Sally Chen</b>, chose pink and blue as the main colours, soft colours that convey a sense of calm and comfort, helping users to feel relaxed, quiet, gentle and happy during use.

Simple interaction design is another major feature. A simple and intuitive interface reduces the cost of learning.

The UI design of the website was done through <b>Figma</b> and all sketches are included in the deliverable folder.https://www.figma.com/design/SqRgaZQaXlgRzC7S6k2ZZA/Drifter?node-id=2%3A352&t=fnpLmyMZOMQvr4Jc-1

Anonymity is a core element of "Drifter". Here, everyone is free to express their true feelings and thoughts without the constraints of identity. This anonymity not only protects the privacy of the users, but also provides a safe environment for them to speak out what would normally be difficult for them to say.

We welcome everyone with a story in their heart to come to "Drifter" and find a place to talk and resonate with each other.

## MVP / Use

1. User registration and login

Allow users to create accounts and log in to secure user information. Users can also log out after using.

2. Change the avatar or keep anonymous

Users can choose to change their avatar or keep the default one.

3. Send notes

Users can send notes anonymously or not, the content can be anything.

4. Receive notes

Users randomly receive secret notes from other users. Plus Users can also search for notes containing specific keywords, such as "love".

5. Anonymous reply

Users can reply anonymously or not to the received note. If the user can't answer or doesn't want to answer the current note, he/she can choose to read the next one.

6. View replies

Users can view the replies received to the notes they send.

6. GPT reply
   For each send notes, user will receive one reply from "Harbor"(ChatGPT 3.5).

### Future Improvements

1. Replies that are read will not appear in the inbox again.
2. Allow users to like or dislike the replies they receive.
3. Users can save their favourite replies to a "favourites" list for later viewing.
4. Set a time after which a note sent by a user will expire and no longer receive a reply.
5. Add appropriate filters to prevent users from posting notices of pornography, gambling, drugs and other social hazards.
6. When random notes are shown, the displayed notes will not be repeated.

## Group Members

| UWA ID   | Name        | Github Username |
| -------- | ----------- | --------------- |
| 23687599 | Sally Chen  | csySally        |
| 23212326 | Lili Liu    | LiliLiu09       |
| 24117922 | Zhengxu Jin | joshjin11       |
| 23495103 | David Pan   | Dave-114-P      |

## How To Launch

To launch this application, follow the steps below. These instructions assume you have Git and Python installed on your system.

### Step 1: Clone the Repository

First, clone the repository to your local machine using Git:

```
git clone https://github.com/LiliLiu09/CITS5505_AgileWebProject2.git
```

```
cd CITS5505_AgileWebProject2
```

### Step 2: Set up a Virtual Environment

```
python -m venv venv
```

Or

```
python3 -m venv venv
```

To activate the virtual environment, use:
-On Windows:

```
.\venv\Scripts\activate
```

-On Unix or MacOS:

```
source venv/bin/activate
```

### Step 3: Install Dependencies

With the virtual environment activated, install the project dependencies using:

```
pip install -r requirements.txt
```

### Step 4: Set Environment Variables

-On Windows:

```
set FLASK_APP=app.py
set FLASK_ENV=development
```

-On Unix or MacOS:

```
export FLASK_APP=app.py
export FLASK_ENV=development
```

### Step 5: Run the Application

```
flask run
```

The application should now be running on http://localhost:5000

## How To Run Tests

-Run unittest:

```
pytest tests
```

-Run Sellenium test:

```
python test_selenium.py
```

## If you want to use GPT generate reply function

```
cd CITS5505_AgileWebProject2/app
```

reivse .env file, replace your OpenAI API key in the file.

```
OPENAI_API_KEY=replace_with_your_openai_api_key
```

## References

[1] [Flask Mega-Tutoria](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)l by Miguel Grinberg.
[2] [Get up and running with the OpenAI API](https://platform.openai.com/docs/quickstart/get-up-and-running-with-the-openai-api)
[3] Insights and assistance provided by ChatGPT, Copilot, a language model by OpenAI.
