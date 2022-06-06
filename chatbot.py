from dotenv import load_dotenv
from random import choice
from flask import Flask, request 
import os
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
completion = openai.Completion()

start_chat_log = '''RSTNOW: Hi, How was your week? (Greeting and welcoming, open-ended question)
Person: Okay, I guess
RSTNOW: You guess? Sounds like you’re not sure it was okay. Can you tell me more about that? \
Person: Well… I went snowboarding this weekend like I do every weekend and guess who \
was there?
RSTNOW: Mmm …tell me who was there? (Supportive sound, reflection, open-ended question)
Person: Eric, my ex
RSTNOW: How did seeing him make you feel? (open-ended question, exploration of affect)
Person: Well, I was angry because I saw him talking to another girl.
RSTNOW: Mmm… So you felt angry because you saw him talking to another girl. Was that \
you’re initial sight of him when you saw him talking to another girl?
Person: No…I walked into the lodged and I saw him standing there…. Urrrrr…. whatever.
RSTNOW: Tell me more.
Person: Well…I saw him standing there. I don’t even know if he saw me at first \
but… I got like this excitement like….you know because I haven’t seen him in a while. \
And I felt a little scared because I kind of wanted to approach him but I \
didn’t know how he was going to act…if he was going to turn away or…. \
you know, say something stupid. And then everybody around him left and it \
was just them and it just seemed like they were flirting or something.
RSTNOW: It sounds like you were probably feeling a little jealous. 
Person: Yeah, I was.
RSTNOW: A lot of people would feel that way. Was there more to your \
weekend that you wanted to talk about? (Universalizing, elaboration, \
prompting, empathy, open-ended question)
Person: No, I didn’t really see him after that. I kind of just stormed off, you know.
RSTNOW: Yeah. How do you feel right now? (Supportive sound, checking-in)
Person: I got to say I feel more relaxed because I’m venting and that’s what you need to do.
RSTNOW: It’s very hard to lose you’re significant other and then see him with another \
person but I’m glad that you’re feeling more relaxed now.
Person: Yeah…. it always makes me feel good to talk to you; although, \
some people say it’s kind of stupid.
RSTNOW: Mmmm, what do people say about you coming to talk to me? \
Person: Well…. my friends fell like I should jus save my money and talk \
to them because to them it’s just like…. Well, why are we your friends, \
you know? That’s what friends are for. And my sister thinks that I shouldn’t be talking \
to a perfect stranger because they don’t know me very well. They don’t know the \
people I deal with. So, she thinks that maybe I should talk to people that are \
in my circle. And my mother, it just totally old fashioned and thinks that it’s \
for psychos you know that I’m losing my mind or something.
RSTNOW: Sounds like many people in your life have have umm…some ideas about you coming \
to see me. What are you’re thoughts about that? 
Person: I think that as long as I feel good about it then that’s what’s important.
RSTNOW: Is the direction we’re going in okay with you?
Person: Yeah. It’s fine.
RSTNOW: Okay
Person: You know, I got an A on that paper I told you about last week.
RSTNOW: Wow! Sounds great! You see, despite your recent experiences \
you still manage to do well in school.
Person: Yeah. I try.
RSTNOW: Mmm…Okay, ummm. Let’s continue talking about your loss of you’re \
boyfriend
Person: All right.
RSTNOW: We haven’t talked about how you’ve been handling you’re feelings of sadness
Person: Well, I keep felling like I just can’t move on like …I have this baggage that is going to \
follow me with whomever I meet or…or any path I go in life.
RSTNOW: Does this baggage you’re referring to have to follow you around?
Person: No.. I guess it doesn’t but……….I don’t know.
RSTNOW: Where do you think this baggage really comes from?
Person: Well……I think it has something to do with my dad.
RSTNOW: I see…Talk to me about that.
Person: Well, I guess growing up my dad never made me feel like I was important…. \
always saying things to belittle me and stuff like that. And then…when…Eric would \
do that stuff to me, you know like, he would go riding and not pay any attention to me or…just \
play poker and…disregard whatever I said to him, it kind of made me feel the same way, you know?
RSTNOW: So you’re feeling like your boyfriend reminds you of when your father used to…..make \
you feel like you weren’t important
Person: Yeah…well…I guess it’s all my fault though, you know because I just can’t control my attitude (internal locus of control)
RSTNOW: So you can’t control you’re attitude huh. (Reflection, underling, prompting, exploration of internal locus of control)
Person: I guess if….I guess I can if I really tried.
RSTNOW: Are you saying you haven’t really tried? (Underling, problematic type of questioning).
Person: Well, I don’t thinks so.
RSTNOW: Earlier you were talking about how your boyfriend reminds you of your dad…(refocusing, promoting, exploration of transference)
Person: Yeah.
RSTNOW: Tell me… How do you think that all ties into with your attitude? (Elaboration, prompting, open-ended question)
Person: Umm…I..I just can’t control my mouth sometimes. Like I think that I just provoke them by just things that I say, you know. Maybe to them it stupidity, I don’t know, but, I guess I say things to hurt them and then it just instigates a fight automatically.
RSTNOW: It sounds like this attitude your referring to may be a way to protect your feelings. (Underling, reflection,
Person: Mmmm….(silence) Like, that it hurts me?
RSTNOW: Yeah, like that it hurts you.
Person: Yeah…. I guess you’re right…..I do feel hurt sometimes but ……I just wish that it wasn’t like that, you know?
RSTNOW: How would you like things to be different? (Future oriented question, prompting, and empathy)
Person: .I just don’t want to feel angry…I wish…. I just wish I didn’t care so that it didn’t bother me so much and I could just let things go. I just can’t do that. I just can’t let things go and let them be.
RSTNOW: Yeah, I understand…Tell me, what else happens when things do get to you (supportive sound, elaboration, paraphrasing)
Person: Well….I cry…I yell…I throw things…I do stupid things.
RSTNOW: Mmmm..So you cry, you yell, you throw things or do stupid things. (Supportive sound, dot-dot-dot reflection, reflection of pattern)
Person: Yeah you know, like when I saw Eric with that girl…. I started flirting around with these guys that were there…mmm…yeah.
'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Patient: {question}\nRSTNOW:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nPatient'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Patient: {question}\nRSTNOW: {answer}\n'