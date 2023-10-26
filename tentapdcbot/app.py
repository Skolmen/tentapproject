import discord
from discord.ext import commands
import datetime
import config
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

api_url = config.API_URL

def update_booking(date, booking_type, room):
    url =  api_url + "/update_booking" 
    
    data = {
        "date": date,
        "type": booking_type,
        "value": room,
    }
    
    response = requests.post(url, json=data)

    if response.status_code != 200:  # Assuming 200 indicates a successful update
        return False
    return True

def parse_parameters(parameters):
    room = ""
    booking_type = ""

    for param in parameters:
        if param.startswith("FM:"):
            room = param.replace("FM:", "").strip()
            booking_type = "FM"
            break
        elif param.startswith("EM:"):
            room = param.replace("EM:", "").strip()
            booking_type = "EM"
            break

    return booking_type, room

def fetch_booking(date):
    url = api_url + "/get_bookings"  # Replace with the actual API endpoint URL

    try:
        response = requests.get(url)
        if response.status_code == 200:
            bookings = response.json()
            for booking in bookings:
                if booking['date'] == date:
                    return {
                        'sal_fm': booking['sal_fm'],
                        'sal_em': booking['sal_em'],
                        'person_1': booking['person_1'],
                        'person_2': booking['person_2']
                    }
            return None  # Booking not found for the given date
        elif response.status_code == 400 or response.status_code == 500:
            return False  # Error in API request or response
        else:
            print("Error fetching bookings:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to the server:", str(e))
        return False

async def get_user_id(name):
    # Prepare the JSON payload
    payload = {
        'name': name
    }

    # Make a POST request to fetch the usernames from the API
    response = requests.post(config.API_URL + "/get_dcuid", json=payload)

    if response.status_code == 200:
        data = response.json()
        user_id = data['dcuid']
        return user_id
    else:
        return None

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

@bot.command()
async def dsalar(ctx):
    today = datetime.date.today()
    result = fetch_booking(str(today))

    if result:
        sal_fm = result['sal_fm']
        sal_em = result['sal_em']
        response = f"Dagens salar är {sal_fm}, FM och {sal_em}, EM"
    elif result is False:
        response = "Ett fel har skett, försök igen senare."
    else:
        response = "Det finns inga bokade salar för idag."

    await ctx.send(response)

@bot.command()
async def isalar(ctx):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    result = fetch_booking(str(tomorrow))

    if result:
        sal_fm = result['sal_fm']
        sal_em = result['sal_em']
        response = f"Morgondagens salar är {sal_fm}, FM och {sal_em}, EM"
    elif result is False:
        response = "Ett fel har skett, försök igen senare."
    else:
        response = "Det finns inga bokade salar för morgondagen."

    await ctx.send(response)

@bot.command()
async def vembokar(ctx):
    two_days_forward = datetime.date.today() + datetime.timedelta(days=2)
    result = fetch_booking(str(two_days_forward))

    if result:
        person_1 = result['person_1']
        person_2 = result['person_2']
        response = f"{person_1}, FM och {person_2}, EM ska boka salar för {two_days_forward}."
    elif result is False:
        response = "Ett fel har skett, försök igen senare."
    else:
        response = f"Det finns ingen som ska boka för {two_days_forward}."

    await ctx.send(response)

@bot.command()
async def boka(ctx):
    link = config.BOOKING_LINK
    response = f"Här är länken för att boka: {link}"
    await ctx.send(response)
    
@bot.command()
async def nybokning(ctx, *parameters):
    two_days_forward = datetime.date.today() + datetime.timedelta(days=2)
    booking_type, room = parse_parameters(parameters)

    if booking_type and room:
        if (update_booking(str(two_days_forward), booking_type, room)):
            response = f"Sal {booking_type} för bokningen två dagar framåt ({str(two_days_forward)}) har uppdaterats."
        else: 
            response = f"Ett fel har skett försök igen senare"
    else:
        response = f"Inget giltigt sal värde angavs. Ange FM:XXX eller EM:XXX"

    await ctx.send(response)
    
@bot.command()
async def hjälp(ctx):
    embed = discord.Embed(title="TentP-robotens kommandon", description="Visar alla kommandon:")
    embed.add_field(name="!dsalar", value="Visar dagens bokade salar.", inline=False)
    embed.add_field(name="!vembokar", value="Visar vem som ska boka sal om 2 dagar.", inline=False)
    embed.add_field(name="!isalar", value="Visar vilka salar som är bokade imorgon.", inline=False)
    embed.add_field(name="!nybokning [parameters]", value="Uppdaterar SAL FM eller SAL EM för bokningen om två dagar.\nParameters: FM:[SAL FM] eller EM:[SAL EM].", inline=False)
    embed.add_field(name="!boka", value="Visar länken för bokning och bokningschema.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def meddelabokare(ctx):
    two_days_forward = datetime.date.today() + datetime.timedelta(days=2)
    result = fetch_booking(str(two_days_forward))

    if result:
        person_1_id = await get_user_id(result['person_1']) #
        person_2_id = await get_user_id(result['person_2']) #
        person_1 = await bot.fetch_user(person_1_id)
        person_2 = await bot.fetch_user(person_2_id)
        mention_1 = person_1 .mention
        mention_2 = person_2.mention
        response = f"{mention_1}, FM och {mention_2}, EM ska boka salar för {two_days_forward}."
    elif result is False:
        response = "Ett fel har skett, försök igen senare."
    else:
        response = f"Det finns ingen som ska boka för {two_days_forward}."

    await ctx.send(response)

# Run the bot
bot.run(config.DISCORD_TOKEN)