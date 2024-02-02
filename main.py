from urllib.parse import urlparse
import base64
import asyncio
import concurrent.futures
import re
from keep_alive import keep_alive
import html
import datetime
import fileinput
import sys
import time
import urllib3
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import aiohttp
import zipfile
import shutil
from PIL import Image
import json
import requests
import string
import random
import io
import os
from discord.ext import commands
import discord
from threading import Thread
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;"><p>kill all soggys</p></body>'''


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()
print("Server Running Because of Axo")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing required arguments, dumbass.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("THAT'S NOT A FUCKING COMMAND LMAO")
    else:
        print(error)


def create_modified_copies(image_path, num_copies, output_folder):
    image = Image.open(image_path)
    width, height = image.size
    file_name, file_extension = os.path.splitext(image_path)

    for i in range(num_copies):
        modified_image = image.copy()

        width, height = modified_image.size

        pixels = modified_image.load()

        channels = len(modified_image.getbands())

        for _ in range(4):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            try:
                if channels == 3:
                    r, g, b = pixels[x, y]
                else:
                    r, g, b, a = pixels[x, y]
                delta = random.randint(-5, 5)
                r = max(0, min(255, r + delta))
                g = max(0, min(255, g + delta))
                b = max(0, min(255, b + delta))
                pixels[x, y] = (r, g, b)
            except TypeError:
                delta = random.randint(0, 30)
                pixels[1, 1] = (max(0, min(255, delta)), max(0, min(255, delta)),
                                max(0, min(255, delta)))
                delta = random.randint(0, 30)
                pixels[1, 149] = (max(0, min(255, delta)), max(0, min(255, delta)),
                                  max(0, min(255, delta)))
                delta = random.randint(0, 30)
                pixels[149, 1] = (max(0, min(255, delta)), max(0, min(255, delta)),
                                  max(0, min(255, delta)))
                delta = random.randint(0, 30)
                pixels[149, 149] = (max(0, min(255, delta)), max(0, min(255, delta)),
                                    max(0, min(255, delta)))
                print("weird image, did the thing lol")
            # time.sleep(0.1)

        modified_image_path = os.path.join(output_folder,
                                           f"{file_name}_{i + 1}{file_extension}")
        modified_image.save(modified_image_path)


@bot.command()
async def bypass(ctx, bait_url: str, input_url: str):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".check" in msg_cnt:

        await message.delete()
    if ".dev" in msg_cnt:

        await message.delete()
    if ".tag" in msg_cnt:

        await message.delete()
    if ".bypass" in msg_cnt:

        await message.delete()
    if ".decal" in msg_cnt:

        await message.delete()
    if ".help" in msg_cnt:

        await message.delete()
    if ".template" in msg_cnt:

        await message.delete()
    if ".upload" in msg_cnt:

        await message.delete()

    await download_image(input_url, "input_image.png")
    if bait_url == "fullclear":
        await download_image(
            "https://cdn.discordapp.com/attachments/1030340602048561182/1195594255121518652/fullclear.png",
            "bait.png")
    else:
        await download_image(bait_url, "bait.png")

    image_path = "input_image.png"
    aimg = Image.open(image_path)
    aimh = aimg.resize((150, 150))
    aimh.save(image_path)
    v_percentages = gpvv(image_path)
    spvv(image_path, v_percentages, 0)
    comb(image_path, "bait.png", image_path)
    os.rename(image_path, f"SPOILER_{image_path}")

    await ctx.send("Here's your processed image:", file=discord.File(f"SPOILER_{image_path}"))

    os.remove(f"SPOILER_{image_path}")
    os.remove(image_path)
    os.remove("bait.png")
    os.remove("random colour.png")


def dtp(image_path, value, brightness, mode):

    img = Image.open(image_path)

    lab_img = img.convert("LAB")

    l_channel, a_channel, b_channel = lab_img.split()

    brightness_enhancer = ImageEnhance.Brightness(l_channel)
    l_channel = brightness_enhancer.enhance(1 + (brightness / 100))

    contrast_enhancer = ImageEnhance.Contrast(l_channel)
    l_channel = contrast_enhancer.enhance(1 + (value / 100))

    new_lab_img = Image.merge("LAB", (l_channel, a_channel, b_channel))

    img = new_lab_img.convert("RGB")

    enhancer = ImageEnhance.Color(img)
    saturation_factor = 1.0
    img = enhancer.enhance(saturation_factor)

    img.save("bnc.png")


def gpvv(image_path):

    img = Image.open(image_path)

    img_hsv = img.convert("HSV")

    width, height = img_hsv.size

    v_values = []

    for x in range(width):
        for y in range(height):

            _, _, v = img_hsv.getpixel((x, y))

            v_values.append(round(v / 255 * 100))

    return v_values


def gray(image_path):
    with Image.open(image_path) as image:

        grayscale_image = image.convert("L")
        grayscale_image.save(image_path)


def spvv(image_path, v_percentages, gravy):
    if gravy == 1:
        dtp(image_path, -100, -85, "blur")
        gray(image_path)

    img = Image.open(image_path)

    img_hsv = img.convert("HSV")

    width, height = img_hsv.size

    new_img = Image.new("HSV", (width, height), (0, 0, 0))

    for x in range(width):
        for y in range(height):

            h, s, _ = img_hsv.getpixel((x, y))

            v = 255

            new_img.putpixel((x, y), (h, s, v))

    new_img_rgba = new_img.convert("RGBA")

    width, height = new_img_rgba.size

    new_new_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    for x in range(width):
        for y in range(height):

            r, g, b, a = new_img_rgba.getpixel((y, x))

            v_percentage = v_percentages[y * width + x]

            alpha = int(v_percentage / 100 * 255)

            new_new_img.putpixel((y, x), (r, g, b, alpha))

    carro = new_new_img.resize((128, 128))
    carro.save(image_path)


def comb(image_path1, image_path2, output):
    a = Image.open(image_path1).convert("RGBA")
    b = Image.open(image_path2).convert("RGBA")

    a = a.resize(b.size)

    result = Image.alpha_composite(b, a)

    result.save(output)


async def download_image(url, filename):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(filename, "wb") as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)
            return filename


@bot.command()
async def decal(ctx, image_link: str, cookie: str):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".check" in msg_cnt:

        await message.delete()
    if ".dev" in msg_cnt:

        await message.delete()
    if ".tag" in msg_cnt:

        await message.delete()
    if ".bypass" in msg_cnt:

        await message.delete()
    if ".decal" in msg_cnt:

        await message.delete()
    if ".help" in msg_cnt:

        await message.delete()
    if ".template" in msg_cnt:

        await message.delete()
    if ".upload" in msg_cnt:

        await message.delete()
    image = await download_image(image_link, "random colour.png")
    upload_num = 6

    def log(text):
        timestamp = datetime.datetime.utcfromtimestamp(
            time.time()).strftime("%H:%M:%S")
        print(f"[{timestamp}] {text}")

    def welcome(session):
        try:
            bot = session.get(
                "https://www.roblox.com/mobileapi/userinfo").json()["UserName"]
            log(f"Welcome `{bot}`")
        except:
            log("Invalid cookie")

    def get_token(session):
        response = session.post(
            "https://friends.roblox.com/v1/users/1/request-friendship")
        if "x-csrf-token" in response.headers:
            return response.headers["x-csrf-token"]
        else:
            log("x-csrf-token not found")
        return veri

    def upload_decal(cookie, location, name, session):
        try:
            headers = {"Requester": "Client",
                       "X-CSRF-TOKEN": get_token(session)}
            response = session.post(
                f"https://data.roblox.com/data/upload/json?assetTypeId=13&name={name}&description=VAULT",
                data=open(location, "rb"),
                headers=headers,
            )
            response.raise_for_status()
            log(f"Uploaded `{name}` successfully")
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                log(f"ratelimited or consequated")
            log(f"Error sending the request")

    with open("useragents.txt", "r") as file:
        useragents = file.read().splitlines()
    for root, dirs, files in os.walk("final"):
        for file in files:
            os.remove(os.path.join(root, file))

    login_api_url = "https://www.roblox.com/mobileapi/userinfo"

    with requests.Session() as session:
        session.cookies.update({".ROBLOSECURITY": cookie})
        welcome(session)
        tmp_folder = "final"
        os.makedirs(tmp_folder, exist_ok=True)
        create_modified_copies(image, upload_num, tmp_folder)
        for root, dirs, files in os.walk("final"):
            for file in files:
                useragent = random.choice(useragents)
                session.headers.update({"User-Agent": useragent})
                name = file
                upload_decal(cookie, os.path.join(
                    "final", file), name, session)
                time.sleep(0.125)

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    response = session.get(login_api_url)
    if response.status_code != 200:
        await ctx.send("Failed to log in. Check your cookie.")
        return

    user_data = response.json()
    username = user_data.get("UserID")
    if not username:
        await ctx.send("Failed to retrieve the username.")
        return
    catalog_url = f"https://www.roblox.com/users/{username}/inventory#!/decals"
    await ctx.send(catalog_url)
    shutil.make_archive("images", "zip", "final")
    time.sleep(1)
    await ctx.send("`FINISHED`", file=discord.File("images.zip"))
    os.remove("random colour.png")


@bot.command()
async def dev(ctx, image_link: str, numbuh: str, cookie: str):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".check" in msg_cnt:

        await message.delete()
    if ".dev" in msg_cnt:

        await message.delete()
    if ".tag" in msg_cnt:

        await message.delete()
    if ".bypass" in msg_cnt:

        await message.delete()
    if ".decal" in msg_cnt:

        await message.delete()
    if ".help" in msg_cnt:

        await message.delete()
    if ".template" in msg_cnt:

        await message.delete()
    if ".upload" in msg_cnt:

        await message.delete()
    image = await download_image(image_link, "random colour.png")
    upload_num = int(numbuh)
    joebiden = ""
    open('accepts.txt', 'w').close()

    session = requests.Session()

    session.cookies.update({".ROBLOSECURITY": cookie})

    headersx = {
        "Accept": "*/*",
        "Cookie": f".ROBLOSECURITY={str(cookie)};"
    }
    responsex = session.post("https://auth.roblox.com/v2/logout",
                             headers=headersx).headers['X-CSRF-TOKEN']

    def unban(session):
        headers = {
            "Accept": "*/*",
            "Cookie": f".ROBLOSECURITY={str(cookie)};",
            "X-Csrf-Token": responsex
        }

        api_url = "https://usermoderation.roblox.com/v1/not-approved/reactivate"

        response = session.post(api_url, headers=headers)
        if response.status_code == 200:
            print("Unbanned Account Successfully")
        else:
            print(f"ERROR CODE {str(response.status_code)}")

    unban(session)

    try:
        bot = session.get(
            "https://www.roblox.com/mobileapi/userinfo").json()["UserID"]
        print(f"Welcome `{bot}`")
    except:
        print("Invalid cookie")

    def log(text):
        timestamp = datetime.datetime.utcfromtimestamp(
            time.time()).strftime("%H:%M:%S")
        print(f"[{timestamp}] {text}")

    def welcome(session):
        try:
            bot = session.get(
                "https://www.roblox.com/mobileapi/userinfo").json()["UserID"]
            log(f"Welcome `{bot}`")
        except:
            log("Invalid cookie")

    def get_token(session):
        response = session.post(
            "https://friends.roblox.com/v1/users/1/request-friendship")
        if "x-csrf-token" in response.headers:
            return response.headers["x-csrf-token"]
        else:
            print("x-csrf-token not found")
            return None

    csrf_token = get_token(session)
    print(csrf_token)

    with open("useragents.txt", "r") as file:
        useragents = file.read().splitlines()
        useragent = random.choice(useragents)
        session.headers.update({"User-Agent": useragent})

    botaaa = session.get(
        "https://www.roblox.com/mobileapi/userinfo").json()["UserID"]
    urlaaa = f"https://games.roblox.com/v2/users/{botaaa}/games"

    responseaaa = requests.get(urlaaa)

    if responseaaa.status_code == 200:

        content = responseaaa.text

        matchaaa = re.search(r"\d+", content)

        if matchaaa:
            numberaaa = matchaaa.group()
            print("Universe ID: " + numberaaa)

        else:
            print("No number found in the content")

    else:
        print(f"Request failed with status code {responseaaa.status_code}")

    def random_alnum(size=2):

        chars = string.ascii_letters
        code = "".join(random.choice(chars) for _ in range(size))
        return code

    headersDP = {
        "Content-Type": "application/json",
        "Cookie": f".ROBLOSECURITY={cookie};",
        "User-Agent": useragent,
        "X-Csrf-Token": csrf_token,
    }

    dataDP = {
        "name": f"vault {str(random_alnum())}",
        "description": "vault",
        "priceInRobux": "1000000000",
    }

    urlDP = f"https://apis.roblox.com/developer-products/v1/universes/{numberaaa}/developerproducts?name=vault_{str(random_alnum())}&description=vault&priceInRobux=1000000000"

    responseDP = requests.post(urlDP, headers=headersDP, json=dataDP)

    content = responseDP.text

    matchbbbc = re.search(r"\d+", content)

    if matchbbbc:
        numberbbbc = matchbbbc.group()
        time.sleep(0.1)
        print("Fake ID: " + numberbbbc)

    else:
        print("No number found in the content")
    time.sleep(0.1)

    numberbbb = session.get(
        f"https://apis.roblox.com/developer-products/v1/developer-products/{str(numberbbbc)}/"
    ).json()["id"]
    print("Real ID: " + str(numberbbb))

    open('ids.txt', 'w').close()
    open('cookie.txt', 'w').close()
    open('cookie.txt', 'a').write(str(cookie))

    def upload_decal(cookie, image_file, name, session):

        headers = {
            "Accept": "*/*",
            "Cookie": f".ROBLOSECURITY={str(cookie)};",
            "User-Agent": useragent,
            "X-Csrf-Token": csrf_token,
        }
        api_url = f"https://apis.roblox.com/developer-products/v1/developer-products/{numberbbb}/image"

        with open(image_file, "rb") as f:
            files = {"imageFile": (image_file, f, "image/png")}
            response = session.post(api_url, headers=headers, files=files)
        if response.status_code == 200:
            content = str(response.json())
            matchbbbca = re.search(r"\d+", content)
            if matchbbbca:
                numberbbbca = matchbbbca.group()
                time.sleep(0.01)
                os.rename(image_file, f'final/{numberbbbca}.png')
                open("ids.txt", "a").write(f"{numberbbbca};")
                # https://develop.roblox.com/v1/assets/16076821176
                # await ctx.send(f"`{numberbbbca};`")

            else:
                print("No number found in the content")
        else:
            print(f"ERROR{str(response.status_code)}")
            # await ctx.send("`BANNED`")

    with open("useragents.txt", "r") as file:
        useragents = file.read().splitlines()
    for root, dirs, files in os.walk("final"):
        for file in files:
            os.remove(os.path.join(root, file))

    login_api_url = "https://www.roblox.com/mobileapi/userinfo"

    with requests.Session() as session:
        session.cookies.update({".ROBLOSECURITY": cookie})
        welcome(session)
        tmp_folder = "final"
        os.makedirs(tmp_folder, exist_ok=True)
        create_modified_copies(image, upload_num, tmp_folder)
        # shutil.make_archive("images", "zip", "final")
        time.sleep(1)

        # await ctx.send(f"# ```SUCCESSFULLY HASHED {upload_num} IMAGES.```",
        # file=discord.File("images.zip"))
        num_threads = int(upload_num)
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_threads) as executor:
            for root, dirs, files in os.walk("final"):
                for file in files:
                    executor.submit(upload_decal, cookie, os.path.join("final", file),
                                    file, session)
        await ctx.send(f"# `SUCCESSFULLY UPLOADED {upload_num} IMAGES.`",
                       file=discord.File("ids.txt"))

    session = requests.Session()
    session.cookies[".ROBLOSECURITY"] = cookie

    response = session.get(login_api_url)
    if response.status_code != 200:
        await ctx.send("Failed to log in. Check your cookie.")
        return

    user_data = response.json()
    username = user_data.get("UserID")
    if not username:
        await ctx.send("Failed to retrieve the username.")
        return
    os.remove("random colour.png")


@bot.command()
async def template(ctx, image_link: str):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".check" in msg_cnt:

        await message.delete()
    if ".dev" in msg_cnt:

        await message.delete()
    if ".tag" in msg_cnt:

        await message.delete()
    if ".bypass" in msg_cnt:

        await message.delete()
    if ".decal" in msg_cnt:

        await message.delete()
    if ".help" in msg_cnt:

        await message.delete()
    if ".template" in msg_cnt:

        await message.delete()
    if ".upload" in msg_cnt:

        await message.delete()
    warlorddada = await download_image(image_link, "temporary.png")
    template = Image.open("template.png")
    temporary = Image.open("temporary.png")
    temporary = temporary.resize((128, 128))
    position = (231, 74)
    template.paste(temporary, position)
    template.save("output.png")
    template.close()
    temporary.close()
    await ctx.send("`FINISHED`", file=discord.File("output.png"))
    os.remove("temporary.png")
    os.remove("output.png")


@bot.command()
async def dyno(ctx, dynx: str):
    fixedd = (dynx.replace("A", "А").replace("a", "а").replace("B", "В").replace(
        "E", "Е").replace("e", "е").replace("3", "З").replace("M", "М").replace(
            "O",
            "О").replace("o", "о").replace("P", "Р").replace("p", "р").replace(
                "C", "С").replace("c", "с").replace("T", "Т").replace(
                    "y", "у").replace("X", "Х").replace("x", "х").replace(
                        "I", "І").replace("i", "і").replace("i", "і").replace(
                            "K", "К").replace("S", "Ѕ").replace(
                                "s", "ѕ").replace("Y", "Ү").replace(
                                    "I", "Ӏ").replace("G", "Ԍ").replace(
                                        "h", "һ").replace("d", "ԁ").replace(
                                            "w", "ԝ").replace("W", "Ԝ").replace(
                                                "Q", "Ԛ").replace(
                                                    "q", "ԛ").replace(
                                                        "H", "Н").replace(
                                                            "u", "u").replace(
                                                                "U", "U"))
    await ctx.send(fixedd)


@bot.command()
async def html(ctx, htmlx: str):

    def encode(s):
        return "".join("&#{:07d};".format(ord(c)) for c in s)

    await ctx.send(
        encode(htmlx).replace("#0000",
                              "#").replace("#000",
                                           "#").replace("#00",
                                                        "#").replace("#0", "#"))


@bot.command()
async def check(ctx):
    open('accepts.txt', 'w').close()
    open('ids.txt', 'w').close()
    if ctx == "cmd":
        async with aiohttp.ClientSession() as session:
            with open('ids.txt', 'r') as file:
                content = str(file.read())

            asset_ids_string = content.rstrip(';')
            asset_ids_list = asset_ids_string.split(";")

            tasks = [
                check_asset(ctx, session, asset_id) for asset_id in asset_ids_list
            ]

            results = await asyncio.gather(*tasks)

            accepted_assets = [
                result for result in results if result is not None]

            if not accepted_assets:
                final_message = "no accepts"
            else:
                newline = "\n"
                final_message = str({newline.join(accepted_assets)})

            print(final_message)
    else:

        message = ctx.message
        msg_cnt = message.content.lower()
        if ".check" in msg_cnt:

            await message.delete()
        if ".dev" in msg_cnt:

            await message.delete()
        if ".tag" in msg_cnt:

            await message.delete()
        if ".bypass" in msg_cnt:

            await message.delete()
        if ".decal" in msg_cnt:

            await message.delete()
        if ".help" in msg_cnt:

            await message.delete()
        if ".template" in msg_cnt:

            await message.delete()
        if ".upload" in msg_cnt:

            await message.delete()
        attachment_url = ctx.message.attachments[0].url
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(attachment_url) as attachment_response:
                    if attachment_response.status == 200:
                        content = await attachment_response.text()

                        open("ids.txt", "a").write(str(content))
                        asset_ids_string = content.rstrip(';')
                        asset_ids_list = asset_ids_string.split(";")

                        tasks = [
                            check_asset(ctx, session, asset_id)
                            for asset_id in asset_ids_list
                        ]

                        results = await asyncio.gather(*tasks)

                        accepted_assets = [
                            result for result in results if result is not None
                        ]

                        if not accepted_assets:
                            final_message = "lmfao you SUCK nothing accepted LOSER"
                        else:
                            newline = ">\n<https://roblox.com/library/"
                            final_message = f"**ACCEPTED ASSETS:**\n<https://roblox.com/library/{newline.join(accepted_assets)}>"

                        await ctx.send(final_message)
                    else:
                        await ctx.send(
                            f"Failed to retrieve the attachment. Status code: {attachment_response.status}"
                        )
            except aiohttp.ClientError as e:
                await ctx.send(f"An error occurred: {e}")


async def check_asset(ctx, session, asset_id):
    asset_api_url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    async with session.get(asset_api_url) as asset_response:
        if asset_response.status == 200:
            open("accepts.txt", "a").write(f"{asset_id};")
            return asset_id
    return None


@bot.command()
async def cmd(ctx):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".cmd" in msg_cnt:
        await message.delete()
    if os.path.getsize('accepts.txt') == 0:
        await check("cmd")
    with open('cookie.txt', 'r') as file:
        cookie = str(file.read())
    with open('accepts.txt', 'r') as file:
        assets = str(file.read())
    numbers = assets.split(';')
    numbers = [num for num in numbers if num]
    asset_id = str(random.choice(numbers))
    session = requests.Session()
    session.cookies.update({".ROBLOSECURITY": str(cookie)})
    with open("useragents.txt", "r") as file:
        useragents = file.read().splitlines()
        useragent = random.choice(useragents)
        session.headers.update({"User-Agent": useragent})
    for line in fileinput.input('accepts.txt', inplace=1):
        sys.stdout.write(line.replace(f'{asset_id};', ''))
    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(f"SPOILER_arzav.png", 'wb') as f:
            f.write(response.content)
        await ctx.send(f"||{str(asset_id)}||", file=discord.File(f"SPOILER_arzav.png"))
        time.sleep(0.69)
        os.remove(f"SPOILER_arzav.png")
    else:
        print(
            f"Failed to download asset with ID {asset_id}. Status code: {response.status_code}"
        )


@bot.command()
async def ad(ctx, url: str, long: str = None):
    if url.isdigit():
        url = f"https://www.roblox.com/library/{url}"

    def get_full_path(url):
        url_parts = urlparse(url)
        path = url_parts.path
        query = url_parts.query
        fragment = url_parts.fragment
        full_path = path.lstrip('/') if path else url
        if query:
            full_path += '?' + query
        if fragment:
            full_path += '#' + fragment
        return full_path

    urlend = str(get_full_path(url))
    print(urlend)
    silly = f"0|/{urlend}"
    sillybytes = silly.encode("ascii")
    base64_bytes = base64.b64encode(sillybytes)
    base64_string = base64_bytes.decode("ascii")
    if long != None:
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        url = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        urlend = str(get_full_path(url))
        print(urlend)
        silly = f"0|/{urlend}"
        sillybytes = silly.encode("ascii")
        base64_bytes = base64.b64encode(sillybytes)
        base64_string = base64_bytes.decode("ascii")
        finalstr = f"https://www.roblox.com/userads/redirect?data={base64_string}0"
        open("ids.txt", "a").write(finalstr)
        await ctx.send("cool", file=discord.File("ids.txt"))
        open('ids.txt', 'w').close()
    else:
        finalstr = f"https://www.roblox.com/userads/redirect?data={ base64_string}0"
        await ctx.send("```" + finalstr + "```")


@bot.command()
async def tag(ctx, image_link: str, pos: str):
    message = ctx.message
    msg_cnt = message.content.lower()
    if ".check" in msg_cnt:

        await message.delete()
    if ".dev" in msg_cnt:

        await message.delete()
    if ".tag" in msg_cnt:

        await message.delete()
    if ".bypass" in msg_cnt:

        await message.delete()
    if ".decal" in msg_cnt:

        await message.delete()
    if ".help" in msg_cnt:

        await message.delete()
    if ".template" in msg_cnt:

        await message.delete()
    if ".upload" in msg_cnt:

        await message.delete()
    await download_image(image_link, "SPOILER_tagtemp.png")
    if pos == "ur":
        comb("tags/upright.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "ul":
        comb("tags/upleft.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "dr":
        comb("tags/downright.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "dl":
        comb("tags/downleft.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "urs":
        comb("tags/ur.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "uls":
        comb("tags/ul.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "drs":
        comb("tags/dr.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    if pos == "dls":
        comb("tags/dl.png", "SPOILER_tagtemp.png", "SPOILER_tagtemp.png")
        await ctx.send("`FINISHED`", file=discord.File("SPOILER_tagtemp.png"))
    else:
        print("ran tag")
    os.remove("SPOILER_tagtemp.png")


@bot.command()
async def url(ctx, url: str):

    def url_encode_all(string):
        encoded = []
        for char in string:
            code = ord(char)
            if str(char) == "=":
                encoded.append("=")
            elif str(char) == "?":
                encoded.append("?")
            elif str(char) == "/":
                encoded.append("/")
            # elif str(char) == ":":
            # encoded.append(":")
            elif str(char) == ".":
                encoded.append(".")
            elif str(char) == "&":
                encoded.append("&")
            else:
                hex = format(code, 'x')
                encoded.append('%' + hex)
        return ''.join(encoded)

    john = str(url_encode_all(url))
    open("ids.txt", "a").write(john)
    await ctx.send("", file=discord.File("ids.txt"))
    open('ids.txt', 'w').close()


bot.run(
    "MTE1NjY0NTkxOTM0NTg4OTMzMA.GKBPX1.wTGfpGWM1kDbSNmsH1rCRTBR-tXluWwg4RxIo4")
