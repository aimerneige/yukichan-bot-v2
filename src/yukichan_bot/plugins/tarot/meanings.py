from typing import TypedDict


class MeaningDetail(TypedDict):
    keywords: str
    description: str


class CardInfo(TypedDict):
    name: str
    upright: MeaningDetail
    reversed: MeaningDetail


# 78 张塔罗牌正/逆位固定释义数据字典 (索引 00-77)
TAROT_MEANINGS: dict[int, CardInfo] = {
    # 大阿卡纳 (00-21)
    0: {
        "name": "愚者 (The Fool)",
        "upright": {"keywords": "新的开始、冒险、自由、可能性", "description": "象征未知的旅程、纯真与勇往直前的精神，适合开启新的尝试。"},
        "reversed": {"keywords": "鲁莽、轻率、逃避、缺乏准备", "description": "提醒注意过于冒失或盲目的决定，缺乏计划可能带来风险。"},
    },
    1: {
        "name": "魔术师 (The Magician)",
        "upright": {"keywords": "创造力、技能、意志力、专注", "description": "意味着你具备实现目标所需的一切资源与能力，行动时机已到。"},
        "reversed": {"keywords": "欺骗、能力未发挥、缺乏自信", "description": "可能存在滥用技能、沟通不畅或计划延迟的情况。"},
    },
    2: {
        "name": "女教皇 (The High Priestess)",
        "upright": {"keywords": "直觉、潜意识、智慧、沉静", "description": "提示倾听内心的声音与直觉，保持沉静与观察。"},
        "reversed": {"keywords": "忽略直觉、肤浅、秘密暴露", "description": "可能忽略了内在警示，或陷入情感封闭与不安中。"},
    },
    3: {
        "name": "女皇 (The Empress)",
        "upright": {"keywords": "丰收获育、母爱、滋养、丰盈", "description": "代表创造力的爆发、情感的滋养与物质生活的丰盈。"},
        "reversed": {"keywords": "依赖、缺乏创造力、过度保护", "description": "提示防范资源浪费、过度依附或情感上的压抑。"},
    },
    4: {
        "name": "皇帝 (The Emperor)",
        "upright": {"keywords": "权威、结构、领导力、稳定", "description": "象征建立秩序与规律，通过自律和坚定领导取得成功。"},
        "reversed": {"keywords": "控制欲强、固执、缺乏约束", "description": "警告避免滥用权力或过于死板固执，学会灵活应变。"},
    },
    5: {
        "name": "教皇 (The Hierophant)",
        "upright": {"keywords": "传统、信仰、学习、指导", "description": "代表对传统智慧的求取、专业指导或社群道德认同。"},
        "reversed": {"keywords": "打破常规、盲从、僵化保守", "description": "暗示质疑传统规范，或防范盲从误导。"},
    },
    6: {
        "name": "恋人 (The Lovers)",
        "upright": {"keywords": "爱与选择、和谐、伙伴关系", "description": "代表深度的情感联结、价值观契合以及重大人生的抉择。"},
        "reversed": {"keywords": "不和谐、抉择困难、价值观冲突", "description": "提示注意伴侣关系中的沟通屏障或不一致的选择。"},
    },
    7: {
        "name": "战车 (The Chariot)",
        "upright": {"keywords": "意志力、胜利、克服障碍、决心", "description": "象征通过自制力与坚定决心战胜困难，取得前进动力。"},
        "reversed": {"keywords": "失控、冲动、方向迷失", "description": "提醒注意冲动盲目带来的挫折，需重拾掌控力。"},
    },
    8: {
        "name": "力量 (Strength)",
        "upright": {"keywords": "内在力量、耐心、包容、勇气", "description": "代表以柔克刚的智慧、强大的内心自控力与慈悲。"},
        "reversed": {"keywords": "自卑、软弱、情绪失控", "description": "可能受到自我怀疑影响，需重建内心的平静与自信。"},
    },
    9: {
        "name": "隐士 (The Hermit)",
        "upright": {"keywords": "反省、探索、内省、寻求真理", "description": "提示适时退隐沉思，通过内在探索寻找真正的答案。"},
        "reversed": {"keywords": "孤立、偏执、过度排外", "description": "警告避免过于孤立自我，陷入固步自封状态。"},
    },
    10: {
        "name": "命运之轮 (Wheel of Fortune)",
        "upright": {"keywords": "转折点、命运、契机、好运", "description": "象征周期的循环与顺应时势带来的正面转变。"},
        "reversed": {"keywords": "阻碍、暂时的低谷、抗拒改变", "description": "处于周期的受限期，需保持耐心迎接转机。"},
    },
    11: {
        "name": "正义 (Justice)",
        "upright": {"keywords": "公平、客观、因果、诚实", "description": "代表理智判断与客观公正，种瓜得瓜种豆得豆。"},
        "reversed": {"keywords": "不公、偏见、逃避责任", "description": "提示警惕非客观裁决或未能承担自身选择的后果。"},
    },
    12: {
        "name": "倒吊人 (The Hanged Man)",
        "upright": {"keywords": "换位思考、顺应、奉献、新视角", "description": "意味着暂时的暂停，以新的视角审视当下方能获得突破。"},
        "reversed": {"keywords": "无谓牺牲、拖延、不愿放弃", "description": "警惕无意义的消耗或固执己见拒绝改变。"},
    },
    13: {
        "name": "死神 (Death)",
        "upright": {"keywords": "结束、转变、新生、告别过去", "description": "象征旧事物的终结与全新阶段的开启，拥抱改变。"},
        "reversed": {"keywords": "抗拒变革、执念、僵局", "description": "难于割舍过去，导致新发展无法顺利萌芽。"},
    },
    14: {
        "name": "节制 (Temperance)",
        "upright": {"keywords": "平衡、调和、自我控制、合作", "description": "代表适度与融洽，善于将不同元素协调为和谐整体。"},
        "reversed": {"keywords": "失衡、极端、缺乏自制", "description": "暗示生活中出现失调，需要重新寻求内外的适度平衡。"},
    },
    15: {
        "name": "恶魔 (The Devil)",
        "upright": {"keywords": "束缚、欲望、执念、物质诱惑", "description": "警惕被负面习惯、物欲或不健康的关系所困束。"},
        "reversed": {"keywords": "觉醒、解脱、摆脱束缚", "description": "意识到瓶颈所在，开始摆脱不良习惯或束缚。"},
    },
    16: {
        "name": "高塔 (The Tower)",
        "upright": {"keywords": "突变、剧变、打破幻想、重新建构", "description": "代表虚假结构的瓦解，突如其来的改变将带来清醒与重塑。"},
        "reversed": {"keywords": "延迟灾难、勉强维持、抗拒真相", "description": "试图避免必然的改变，反而延长了不稳定的状态。"},
    },
    17: {
        "name": "星星 (The Star)",
        "upright": {"keywords": "希望、灵感、宁静、治愈", "description": "带来充沛的希望与灵感，经历风雨后迎来心灵的平静。"},
        "reversed": {"keywords": "灰心、绝望、信心动摇", "description": "暂时失去了远景，需重新点燃内在信念。"},
    },
    18: {
        "name": "月亮 (The Moon)",
        "upright": {"keywords": "潜意识、不安、迷茫、幻觉", "description": "代表隐藏的隐患或情绪上的波动，需看清迷雾背后的真相。"},
        "reversed": {"keywords": "迷雾散去、解开误会、克服恐惧", "description": "隐藏的事物开始显现，迷茫与不安逐步消散。"},
    },
    19: {
        "name": "太阳 (The Sun)",
        "upright": {"keywords": "光明、成功、喜悦、活力", "description": "充满正能量与光明，万事顺遂，成果喜人。"},
        "reversed": {"keywords": "暂时阴霾、过于乐观、热情减退", "description": "成功可能略有延迟，但整体大势依然积极。"},
    },
    20: {
        "name": "审判 (Judgement)",
        "upright": {"keywords": "召唤、觉醒、自我总结、重生", "description": "代表关键时刻的清算与反思，听从内心的召唤走向新阶段。"},
        "reversed": {"keywords": "自我怀疑、悔恨、拖延裁决", "description": "因犹豫不决或逃避评估而错失重生的契机。"},
    },
    21: {
        "name": "世界 (The World)",
        "upright": {"keywords": "圆满、完成、成功、融合", "description": "象征周期的完美闭环与目标的终极达成，内心充满安宁。"},
        "reversed": {"keywords": "未臻完善、延期完成、缺乏闭环", "description": "距离理想终点尚差临门一脚，需补充最后细节。"},
    },
}


def _get_minor_arcana_info(index: int) -> CardInfo:
    suit_names = ["权杖", "钱币", "圣杯", "宝剑"]
    suit_eng = ["Wands", "Pentacles", "Cups", "Swords"]
    suit_idx = (index - 22) // 14
    num_idx = (index - 22) % 14

    suit = suit_names[suit_idx]
    s_eng = suit_eng[suit_idx]

    rank_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "侍者", "骑士", "王后", "国王"]
    r_name = rank_names[num_idx]

    name = f"{suit}{r_name} ({s_eng} {r_name})"

    upright_desc = f"{suit}元素的正向能量呈现，代表在相关事务上的进展、动力与积极成果。"
    reversed_desc = f"{suit}元素的受阻或过度呈现，提示需要注意调节与防范相应偏差。"

    return {
        "name": name,
        "upright": {"keywords": f"{suit}、进展、积极", "description": upright_desc},
        "reversed": {"keywords": f"{suit}受阻、偏差、调整", "description": reversed_desc},
    }


def get_card_info(card_index: int) -> CardInfo:
    if card_index in TAROT_MEANINGS:
        return TAROT_MEANINGS[card_index]
    if 22 <= card_index <= 77:
        return _get_minor_arcana_info(card_index)
    return {
        "name": f"神秘塔罗牌 ({card_index})",
        "upright": {"keywords": "未知", "description": "牌面蕴含神秘的启示。"},
        "reversed": {"keywords": "未知", "description": "逆向能量等待进一步洞察。"},
    }


def format_card_meaning(card_filename: str, is_upright: bool) -> str:
    try:
        prefix = card_filename.split("_")[0]
        card_index = int(prefix)
    except (ValueError, IndexError):
        card_index = 0

    info = get_card_info(card_index)
    orientation = "正位" if is_upright else "逆位"
    meaning_detail = info["upright"] if is_upright else info["reversed"]

    return (
        f"【{info['name']} - {orientation}】\n"
        f"关键词：{meaning_detail['keywords']}\n"
        f"解析：{meaning_detail['description']}"
    )
