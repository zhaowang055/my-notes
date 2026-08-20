#!/usr/bin/env python3
"""Convert Feishu lark-table and callout tags to standard HTML."""
import re

def convert_lark_tables(html):
    pattern = r'<p><lark-table[^>]*></p>(.*?)<p></lark-table></p>'

    def replace_table(match):
        content = match.group(1)
        rows = []
        row_pattern = r'<p>\s*<lark-tr>\s*</p>(.*?)<p>\s*</lark-tr>\s*</p>'
        for row_match in re.finditer(row_pattern, content, re.DOTALL):
            row_content = row_match.group(1)
            cells = []
            cell_pattern = r'<p>\s*<lark-td>\s*</p>(.*?)<p>\s*</lark-td>\s*</p>'
            for cell_match in re.finditer(cell_pattern, row_content, re.DOTALL):
                cell_text = cell_match.group(1).strip()
                cell_text = re.sub(r'^<p>(.*?)</p>$', r'\1', cell_text, flags=re.DOTALL)
                cell_text = re.sub(r'\s+', ' ', cell_text).strip()
                cells.append(cell_text)
            rows.append(cells)

        if not rows:
            return match.group(0)

        lines = ['<div class="table-wrap"><table>']
        lines.append('  <thead><tr>')
        for cell in rows[0]:
            lines.append(f'    <th>{cell}</th>')
        lines.append('  </tr></thead>')
        if len(rows) > 1:
            lines.append('  <tbody>')
            for row in rows[1:]:
                lines.append('  <tr>')
                for cell in row:
                    lines.append(f'    <td>{cell}</td>')
                lines.append('  </tr>')
            lines.append('  </tbody>')
        lines.append('</table></div>')
        return '\n'.join(lines)

    return re.sub(pattern, replace_table, html, flags=re.DOTALL)


def convert_callouts(html):
    # Map emoji names to actual emoji and color classes
    emoji_map = {
        'bulb': '💡',
        'books': '📚',
        'dart': '🎯',
        'warning': '⚠️',
        'check': '✅',
        'cross': '❌',
        'star': '⭐',
        'fire': '🔥',
        'rocket': '🚀',
        'memo': '📝',
        'pushpin': '📌',
        'wrench': '🔧',
        'gear': '⚙️',
        'magnifying': '🔍',
        'link': '🔗',
        'bell': '🔔',
        'calendar': '📅',
        'clock': '🕐',
        'heart': '❤️',
        'thumbsup': '👍',
        'clap': '👏',
        'wave': '👋',
        'thinking': '🤔',
        'eyes': '👀',
        'lightning': '⚡',
        'key': '🔑',
        'lock': '🔒',
        'unlock': '🔓',
        'shield': '🛡️',
        'target': '🎯',
        'chart': '📊',
        'money': '💰',
        'gift': '🎁',
        'trophy': '🏆',
        'medal': '🥇',
        'crown': '👑',
        'diamond': '💎',
        'gem': '💎',
        'crystal': '🔮',
        'magic': '✨',
        'sparkle': '✨',
        'boom': '💥',
        'collision': '💥',
        'zap': '⚡',
        'snowflake': '❄️',
        'sun': '☀️',
        'moon': '🌙',
        'star2': '🌟',
        'rainbow': '🌈',
        'cloud': '☁️',
        'umbrella': '☂️',
        'rain': '🌧️',
        'thunder': '⛈️',
        'tornado': '🌪️',
        'ocean': '🌊',
        'mountain': '⛰️',
        'earth': '🌍',
        'globe': '🌐',
        'map': '🗺️',
        'compass': '🧭',
        'pin': '📍',
        'flag': '🚩',
        'banner': '🚩',
        'ribbon': '🎀',
        'balloon': '🎈',
        'party': '🎉',
        'confetti': '🎊',
        'tada': '🎉',
        'fireworks': '🎆',
        'sparkler': '🎇',
        'balloon2': '🎈',
        'gift2': '🎁',
        'birthday': '🎂',
        'cake': '🎂',
        'cookie': '🍪',
        'candy': '🍬',
        'lollipop': '🍭',
        'chocolate': '🍫',
        'icecream': '🍦',
        'ice_cream': '🍦',
        'donut': '🍩',
        'pizza': '🍕',
        'hamburger': '🍔',
        'fries': '🍟',
        'hotdog': '🌭',
        'taco': '🌮',
        'burrito': '🌯',
        'sushi': '🍣',
        'ramen': '🍜',
        'spaghetti': '🍝',
        'soup': '🍲',
        'salad': '🥗',
        'popcorn': '🍿',
        'corn': '🌽',
        'grape': '🍇',
        'melon': '🍈',
        'watermelon': '🍉',
        'orange': '🍊',
        'lemon': '🍋',
        'banana': '🍌',
        'apple': '🍎',
        'green_apple': '🍏',
        'pear': '🍐',
        'peach': '🍑',
        'cherry': '🍒',
        'strawberry': '🍓',
        'kiwi': '🥝',
        'tomato': '🍅',
        'coconut': '🥥',
        'avocado': '🥑',
        'eggplant': '🍆',
        'potato': '🥔',
        'carrot': '🥕',
        'corn2': '🌽',
        'hot_pepper': '🌶️',
        'cucumber': '🥒',
        'broccoli': '🥦',
        'mushroom': '🍄',
        'peanuts': '🥜',
        'chestnut': '🌰',
        'bread': '🍞',
        'croissant': '🥐',
        'baguette': '🥖',
        'pretzel': '🥨',
        'pancakes': '🥞',
        'cheese': '🧀',
        'meat': '🥩',
        'poultry': '🍗',
        'cut_of_meat': '🥩',
        'bacon': '🥓',
        'hamburger2': '🍔',
        'fries2': '🍟',
        'pizza2': '🍕',
        'hotdog2': '🌭',
        'sandwich': '🥪',
        'taco2': '🌮',
        'burrito2': '🌯',
        'stuffed_flatbread': '🥙',
        'falafel': '🧆',
        'egg': '🥚',
        'cooking': '🍳',
        'shallow_pan_of_food': '🥘',
        'pot_of_food': '🍲',
        'fondue': '🫕',
        'bowl_with_spoon': '🥣',
        'green_salad': '🥗',
        'popcorn2': '🍿',
        'butter': '🧈',
        'salt': '🧂',
        'canned_food': '🥫',
        'bento': '🍱',
        'rice_cracker': '🍘',
        'rice_ball': '🍙',
        'rice': '🍚',
        'curry': '🍛',
        'steaming_bowl': '🍜',
        'spaghetti2': '🍝',
        'roasted_sweet_potato': '🍠',
        'oden': '🍢',
        'sushi2': '🍣',
        'fried_shrimp': '🍤',
        'fish_cake': '🍥',
        'moon_cake': '🥮',
        'dango': '🍡',
        'dumpling': '🥟',
        'fortune_cookie': '🥠',
        'takeout_box': '🥡',
        'crab': '🦀',
        'lobster': '🦞',
        'shrimp': '🦐',
        'squid': '🦑',
        'oyster': '🦪',
        'soft_ice_cream': '🍦',
        'shaved_ice': '🍧',
        'ice_cream2': '🍨',
        'doughnut': '🍩',
        'cookie2': '🍪',
        'birthday_cake': '🎂',
        'shortcake': '🍰',
        'cupcake': '🧁',
        'pie': '🥧',
        'chocolate_bar': '🍫',
        'candy2': '🍬',
        'lollipop2': '🍭',
        'custard': '🍮',
        'honey_pot': '🍯',
        'baby_bottle': '🍼',
        'milk': '🥛',
        'hot_beverage': '☕',
        'teacup': '🍵',
        'sake': '🍶',
        'champagne': '🍾',
        'wine_glass': '🍷',
        'cocktail': '🍸',
        'tropical_drink': '🍹',
        'beer': '🍺',
        'beers': '🍻',
        'clinking_glasses': '🥂',
        'tumbler_glass': '🥃',
        'cup_with_straw': '🥤',
        'bubble_tea': '🧋',
        'beverage_box': '🧃',
        'mate': '🧉',
        'ice_cube': '🧊',
        'chopsticks': '🥢',
        'plate_with_cutlery': '🍽️',
        'fork_and_knife': '🍴',
        'spoon': '🥄',
        'kitchen_knife': '🔪',
        'amphora': '🏺',
        'earth_africa': '🌍',
        'earth_americas': '🌎',
        'earth_asia': '🌏',
        'globe_with_meridians': '🌐',
        'world_map': '🗺️',
        'compass2': '🧭',
        'snow_capped_mountain': '🏔️',
        'mountain2': '⛰️',
        'volcano': '🌋',
        'mount_fuji': '🗻',
        'camping': '🏕️',
        'beach_with_umbrella': '🏖️',
        'desert': '🏜️',
        'desert_island': '🏝️',
        'national_park': '🏞️',
        'stadium': '🏟️',
        'classical_building': '🏛️',
        'building_construction': '🏗️',
        'bricks': '🧱',
        'rock': '🪨',
        'wood': '🪵',
        'hut': '🛖',
        'houses': '🏘️',
        'derelict_house': '🏚️',
        'house': '🏠',
        'house_with_garden': '🏡',
        'office': '🏢',
        'post_office': '🏣',
        'european_post_office': '🏤',
        'hospital': '🏥',
        'bank': '🏦',
        'hotel': '🏨',
        'love_hotel': '🏩',
        'convenience_store': '🏪',
        'school': '🏫',
        'department_store': '🏬',
        'factory': '🏭',
        'japanese_castle': '🏯',
        'european_castle': '🏰',
        'wedding': '💒',
        'tokyo_tower': '🗼',
        'statue_of_liberty': '🗽',
        'church': '⛪',
        'mosque': '🕌',
        'hindu_temple': '🛕',
        'synagogue': '🕍',
        'shinto_shrine': '⛩️',
        'kaaba': '🕋',
        'fountain': '⛲',
        'tent': '⛺',
        'foggy': '🌁',
        'night_with_stars': '🌃',
        'cityscape': '🏙️',
        'sunrise_over_mountains': '🌄',
        'sunrise': '🌅',
        'city_sunset': '🌆',
        'city_sunrise': '🌇',
        'bridge_at_night': '🌉',
        'hotsprings': '♨️',
        'carousel_horse': '🎠',
        'playground_slide': '🛝',
        'ferris_wheel': '🎡',
        'roller_coaster': '🎢',
        'barber': '💈',
        'circus_tent': '🎪',
        'locomotive': '🚃',
        'railway_car': '🚃',
        'high_speed_train': '🚄',
        'bullet_train': '🚅',
        'train': '🚆',
        'metro': '🚇',
        'light_rail': '🚈',
        'station': '🚉',
        'tram': '🚊',
        'monorail': '🚝',
        'mountain_railway': '🚞',
        'tram_car': '🚋',
        'bus': '🚌',
        'oncoming_bus': '🚍',
        'trolleybus': '🚎',
        'minibus': '🚐',
        'ambulance': '🚑',
        'fire_engine': '🚒',
        'police_car': '🚓',
        'oncoming_police_car': '🚔',
        'taxi': '🚕',
        'oncoming_taxi': '🚖',
        'automobile': '🚗',
        'oncoming_automobile': '🚘',
        'sport_utility_vehicle': '🚙',
        'pickup_truck': '🛻',
        'delivery_truck': '🚚',
        'articulated_lorry': '🚛',
        'tractor': '🚜',
        'racing_car': '🏎️',
        'motorcycle': '🏍️',
        'motor_scooter': '🛵',
        'manual_wheelchair': '🦽',
        'motorized_wheelchair': '🦼',
        'auto_rickshaw': '🛺',
        'bike': '🚲',
        'kick_scooter': '🛴',
        'skateboard': '🛹',
        'roller_skate': '🛼',
        'bus_stop': '🚏',
        'motorway': '🛣️',
        'railway_track': '🛤️',
        'oil_drum': '🛢️',
        'fuelpump': '⛽',
        'wheel': '🛞',
        'rotating_light': '🚨',
        'traffic_light': '🚥',
        'vertical_traffic_light': '🚦',
        'stop_sign': '🛑',
        'construction': '🚧',
        'anchor': '⚓',
        'ring_buoy': '🛟',
        'sailboat': '⛵',
        'canoe': '🛶',
        'speedboat': '🚤',
        'passenger_ship': '🛳️',
        'ferry': '⛴️',
        'motor_boat': '🛥️',
        'ship': '🚢',
        'airplane': '✈️',
        'small_airplane': '🛩️',
        'airplane_departure': '🛫',
        'airplane_arrival': '🛬',
        'parachute': '🪂',
        'seat': '💺',
        'helicopter': '🚁',
        'suspension_railway': '🚟',
        'mountain_cableway': '🚠',
        'aerial_tramway': '🚡',
        'artificial_satellite': '🛰️',
        'rocket': '🚀',
        'flying_saucer': '🛸',
        'bellhop_bell': '🛎️',
        'luggage': '🧳',
        'hourglass_done': '⌛',
        'hourglass': '⏳',
        'watch': '⌚',
        'alarm_clock': '⏰',
        'stopwatch': '⏱️',
        'timer_clock': '⏲️',
        'mantelpiece_clock': '🕰️',
        'clock12': '🕛',
        'clock1230': '🕧',
        'clock1': '🕐',
        'clock130': '🕜',
        'clock2': '🕑',
        'clock230': '🕝',
        'clock3': '🕒',
        'clock330': '🕞',
        'clock4': '🕓',
        'clock430': '🕟',
        'clock5': '🕔',
        'clock530': '🕠',
        'clock6': '🕕',
        'clock630': '🕡',
        'clock7': '🕖',
        'clock730': '🕢',
        'clock8': '🕗',
        'clock830': '🕣',
        'clock9': '🕘',
        'clock930': '🕤',
        'clock10': '🕙',
        'clock1030': '🕥',
        'clock11': '🕚',
        'clock1130': '🕦',
        'new_moon': '🌑',
        'waxing_crescent_moon': '🌒',
        'first_quarter_moon': '🌓',
        'waxing_gibbous_moon': '🌔',
        'full_moon': '🌕',
        'waning_gibbous_moon': '🌖',
        'last_quarter_moon': '🌗',
        'waning_crescent_moon': '🌘',
        'crescent_moon': '🌙',
        'new_moon_with_face': '🌚',
        'first_quarter_moon_with_face': '🌛',
        'last_quarter_moon_with_face': '🌜',
        'thermometer': '🌡️',
        'sun': '☀️',
        'full_moon_with_face': '🌝',
        'sun_with_face': '🌞',
        'ringed_planet': '🪐',
        'star': '⭐',
        'glowing_star': '🌟',
        'shooting_star': '🌠',
        'milky_way': '🌌',
        'cloud': '☁️',
        'sun_behind_cloud': '⛅',
        'cloud_with_lightning_and_rain': '⛈️',
        'sun_behind_small_cloud': '🌤️',
        'sun_behind_large_cloud': '🌥️',
        'sun_behind_rain_cloud': '🌦️',
        'cloud_with_rain': '🌧️',
        'cloud_with_snow': '🌨️',
        'cloud_with_lightning': '🌩️',
        'tornado': '🌪️',
        'fog': '🌫️',
        'wind_face': '🌬️',
        'cyclone': '🌀',
        'rainbow': '🌈',
        'closed_umbrella': '🌂',
        'umbrella': '☂️',
        'umbrella_with_rain_drops': '☔',
        'umbrella_on_ground': '⛱️',
        'high_voltage': '⚡',
        'snowflake': '❄️',
        'snowman': '☃️',
        'snowman_without_snow': '⛄',
        'comet': '☄️',
        'fire': '🔥',
        'droplet': '💧',
        'water_wave': '🌊',
    }

    # Background color to CSS class mapping
    bg_map = {
        'light-blue': 'callout-blue',
        'blue': 'callout-blue',
        'light-yellow': 'callout-yellow',
        'yellow': 'callout-yellow',
        'light-green': 'callout-green',
        'green': 'callout-green',
        'light-orange': 'callout-orange',
        'orange': 'callout-orange',
        'light-red': 'callout-orange',
        'red': 'callout-orange',
    }

    # Pattern: <p><callout emoji="xxx" background-color="yyy"></p> ... <p></callout></p>
    pattern = r'<p><callout\s+emoji="([^"]*)"[^>]*></p>(.*?)<p></callout></p>'

    def replace_callout(match):
        emoji_name = match.group(1)
        content = match.group(2).strip()

        # Get actual emoji
        emoji = emoji_map.get(emoji_name, '💡')

        # Get background color from the original tag
        full_tag = match.group(0)
        bg_match = re.search(r'background-color="([^"]*)"', full_tag)
        bg_color = bg_match.group(1) if bg_match else 'light-blue'
        css_class = bg_map.get(bg_color, 'callout-blue')

        # Clean up content - remove wrapping <p> tags, join lines
        content = re.sub(r'</?p>', '', content)
        content = re.sub(r'\s+', ' ', content).strip()

        return f'<div class="callout {css_class}">{emoji} {content}</div>'

    return re.sub(pattern, replace_callout, html, flags=re.DOTALL)


# Read file
with open('claude-code-guide.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Convert tables
converted = convert_lark_tables(html)
table_count = html.count('<lark-table') - converted.count('<lark-table')
print(f"Converted {table_count} lark-table blocks")

# Convert callouts
converted = convert_callouts(converted)
callout_count = html.count('<callout') - converted.count('<callout')
print(f"Converted {callout_count} callout blocks")

# Add table and callout styles if not present
if '<table' in converted and 'border-collapse' not in converted:
    table_style = """
  .table-wrap { overflow-x: auto; margin: 16px 0; }
  table { border-collapse: collapse; width: 100%; font-size: 0.9em; }
  th, td { border: 1px solid var(--border); padding: 10px 14px; text-align: left; }
  th { background: var(--bg-table-header, #f1f5f9); font-weight: 600; }
  tr:nth-child(even) td { background: var(--bg-table-alt, #f8fafc); }
"""
    converted = converted.replace('</style>', table_style + '</style>')
    print("Added table styles")

if '<div class="callout' in converted and '.callout {' not in converted:
    callout_style = """
  .callout {
    padding: 16px 20px; border-radius: 8px; margin: 20px 0;
    font-size: 0.95rem; line-height: 1.7; border-left: 4px solid;
  }
  .callout-blue { background: var(--bg-callout-blue, #EFF6FF); border-color: var(--accent, #2563EB); }
  .callout-yellow { background: var(--bg-callout-yellow, #FFFBEB); border-color: #F59E0B; }
  .callout-green { background: var(--bg-callout-green, #F0FDF4); border-color: #22C55E; }
  .callout-orange { background: var(--bg-callout-orange, #FFF7ED); border-color: #F97316; }
"""
    # Add dark mode callout colors
    callout_dark = """
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg-callout-blue: #172554; --bg-callout-yellow: #422006;
      --bg-callout-green: #052E16; --bg-callout-orange: #431407;
    }
  }
  :root[data-theme="dark"] {
    --bg-callout-blue: #172554; --bg-callout-yellow: #422006;
    --bg-callout-green: #052E16; --bg-callout-orange: #431407;
  }
"""
    converted = converted.replace('</style>', callout_style + callout_dark + '</style>')
    print("Added callout styles")

# Write back
with open('claude-code-guide.html', 'w', encoding='utf-8') as f:
    f.write(converted)

print("Done!")
