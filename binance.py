import telepot
import requests
import time

# Replace with your Telegram Bot Token
BOT_TOKEN = '6559635014:AAGl99mEc1Jb0pc31MHWAkbhui2cvwpWbCI'

# Define the chat ID where you want to send notifications
CHAT_ID = '6613211769'

# BscScan API Key
API_KEY = 'UKKSVEYEBDMX6CJSTVFJEKT8BWPNGZDCZN'

# BscScan API URL
API_URL = 'https://api.bscscan.com/api'

# Dictionary to store the last checked block number for each wallet address
last_checked_blocks = {}

def get_current_block_number():
    params = {'module': 'proxy', 'action': 'eth_blockNumber', 'apikey': API_KEY}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        current_block = int(response.json().get('result', '0x0'), 16)
        return current_block
    else:
        print(f"Error fetching current block number: HTTP {response.status_code}")
        return None

def get_latest_token_transfer(address):
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': address,
        'page': 1,
        'offset': 1,
        'startblock': last_checked_blocks.get(address, 0) + 1,
        'endblock': 'latest',
        'sort': 'asc',
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        result = response.json().get('result', [])
        if result:
            return result[0]
        else:
            return None
    else:
        print(f"Error fetching transactions: HTTP {response.status_code}")
        return None

bot = telepot.Bot(BOT_TOKEN)

def send_notification(chat_id, message):
    bot.sendMessage(chat_id, message, parse_mode="Markdown")

def monitor_wallet_addresses():
    wallet_addresses = [
        "0x136D02dC8Af604a5f943BE670F826B6cd5B9B660",
        "0xE99bC90D3Cb86cf095D75a020C10FBF9D4aA9A4D",
        "0xc77D249809ae5A118eEf66227d1A01A3D62c82d4",
        "0x66F6d639199342619CAF8617bf80eA738e5960A3",
        "0x699255686B24980EB3Ea3Bd84FBb62Fd42954064",
        "0xE934116a4073E476C848d0db704606010146B4c2",
        "0x57f2819c959AbBcF22623d5ec1d3164b213E9711",
        "0x32F24a55224be5B38eD3E17eA5e3d512A6cEe5d6",
        "0x56DB61E267C8a033071135Aed1Acf47c4a0eF09c",
        "0xf8e6f23f18a04Bfd481cE71ac894488568285f1b",
        "0x47ED586099a29BD015D5Ec639cE06BD09ee091C2",
        "0xb8e38504A8F19bbF6ebF6D9f6E4efB1127DC2A7d",
        "0x4823BE7F266c5bcA85B7Dbd8e41f4710e1c49a7b",
        "0xB290Fd44A628A21FCCBf6347668D80dE4177dA42",
        "0x068C53aaFBFEB51bf1E75b88f16aF22B448F8E8c",
        "0x1f5bbEf0722b6188B87b29DFf530d6cfb5A46967",
        "0x7A1Bc720dF62548DA60EC2a2b0313B9b65cA894B",
        "0x9B7D7c4ce98036c4d6F3D638a00e220e083116c7",
        "0x84a25aa392835B05E66b85D2D03aC32F2C4A9c13",
        "0x675E11a29dFB3C99A83d3700cb3f255e88EC48A0",
        "0x1119C4ce8F56d96a51b5A38260Fede037C7126F5",
        "0xBE676A680343DE114f7e71DF9397bDEAbe77551e",
        "0xC74b209fe38EcED29105C802FfB4BA280895546A",
        "0xa35E1842447c330771A572B72ceeD0bA556336E3",
        "0x6e40445B193dfA5a4295F532D001ad56B0a3e395",
        "0x75056c3553B9b563b8979177f9637e4caCc78a88",
        "0x394669e81371BbEA86Ce29174Abf81DA71B3D851",
        "0x832a2D107D0C1df54113Ed7A086c2bdfb126388e",
        "0xff677b13E9ae5F86E3Ab7203fb0F37d59d45Dc7E",
        "0x5f7c629EDAB4d1cdAffa878382b0FA419261300d",
        "0xC4E40a6cE1e0e4FF9b947c607Bb9CaB1314361C8",
        "0xF642e82500e058E45D02e20c00fa1e668be158e3",
        "0xda862888A919B743822D34CD0017c073950AE0CD",
        "0x60Ef2646d561121DC15bCd020c2FD5A8761c105f",
        "0x4949f91b67C969185c471Aac26F43767a0766Dbf",
        "0xb79f144418EAf73452ac0CB8B8789ED1388Dc3C4",
        "0x80Ca27268d4603E00B8d4D98Aa309dB438127d19",
        "0x464bd958709bEd9599e4cAFaAE7fC0115B80a47c",
        "0xB7d75e7b4865447103B4214726AE933D13866F99",
        "0x577314613Bf23c4d7f0BdAe7151c9c5EAB0CA532",
        "0xAA24a8AdCf9f26541C1Da07f480aBD32f7c928bE",
        "0x0743Ccffa829697b3d9241a464b9E22F10664A2b",
        "0xbFA616C9779FA08D9b6c928B4A9c63a2d635a50d",
        "0xBEabc50C4F42Fe460B50cD8b9c9587153e5f8A3c",
        "0x38dDEf6Bd12368e21C4de879BD6B3915EbF528E4",
        "0x69c1240100eF812C6caDD4bDC02ad00473862d6a",
        "0x0fd7473151aFc41a4F7c2bD06DB5A403AFd4aAfe",
        "0x3c28EBf05F5Fd3F7C683022B386EBDd63c1dC11A"
        # Add your wallet addresses here
    ]

    current_block = get_current_block_number()
    if current_block:
        for address in wallet_addresses:
            last_checked_blocks[address] = current_block

    while True:
        time.sleep(30)  # Delay for API rate limit considerations
        for address in wallet_addresses:
            latest_tx = get_latest_token_transfer(address)
            if latest_tx and isinstance(latest_tx, dict) and 'blockNumber' in latest_tx:
                block_number = int(latest_tx['blockNumber'], 16)
                if address not in last_checked_blocks or block_number > last_checked_blocks[address]:
                    message = (
                        f"🚀 *New Transaction on BSC* 🚀\n\n"
                        f"🔹 *Address*: [{address}](https://bscscan.com/address/{address})\n"
                        f"🔹 *Direction*: {'Received' if address.lower() == latest_tx.get('to', '').lower() else 'Sent'}\n"
                        f"🔹 *Token*: {latest_tx.get('tokenName', 'Unknown Token')} ({latest_tx.get('tokenSymbol', 'N/A')})\n"
                        f"🔹 *Value*: {latest_tx.get('value', 'N/A')}\n"
                        f"🔹 *Block Number*: {block_number}\n"
                    )
                    send_notification(CHAT_ID, message)
                    last_checked_blocks[address] = block_number

if __name__ == '__main__':
    monitor_wallet_addresses()
