from ..info import get_card_set
from ..config import prob1,prob2
from random import randint as r,choice as r1

async def rolls(time:dict,leader:dict,alternate:dict,cards:dict,only_leader:bool,only_legend:bool,no_bronze:bool):
    """
    确定具体卡牌
    """
    leadercard = []
    card = {1:[],2:[],3:[],4:[]}
    legend_leader_card = []
    legend_alternate_card = []
    gold_alternate_card = []
    gold_leader_card = []
    silver_leader_card = []
    silver_alternate_card = []
    bronze_leader_card = []
    bronze_alternate_card = []
    legend_leader_prob = 0
    gold_leader_prob = 0
    silver_leader_prob = 0
    bronze_leader_prob = 0
    legend_alternate_prob = 0
    gold_alternate_prob = 0
    silver_alternate_prob = 0
    bronze_alternate_prob = 0
    for i in leader[1]:
        legend_leader_prob += leader[1][i]
        for j in range(0,leader[1][i]):
            legend_leader_card.append(i)
    for i in alternate[1]:
        legend_alternate_prob += alternate[1][i]
        for j in range(0,alternate[1][i]):
            legend_alternate_card.append(i)
    for i in leader[2]:
        gold_leader_prob += leader[2][i]
        for j in range(0,leader[2][i]):
            gold_leader_card.append(i)
    for i in leader[3]:
        silver_leader_prob += leader[3][i]
        for j in range(0,leader[3][i]):
            silver_leader_card.append(i)
    for i in leader[4]:
        bronze_leader_prob += leader[4][i]
        for j in range(0,leader[4][i]):
            bronze_leader_card.append(i)
    if not only_legend:
        for i in alternate[2]:
            gold_alternate_prob += alternate[2][i]
            for j in range(0,alternate[2][i]):
                gold_alternate_card.append(i)
        for i in alternate[3]:
            silver_alternate_prob += alternate[3][i]
            for j in range(0,alternate[3][i]):
                silver_alternate_card.append(i)
        for i in alternate[4]:
            bronze_alternate_prob += alternate[4][i]
            for j in range(0,alternate[4][i]):
                bronze_alternate_card.append(i)
        if time[1]:
            for i in range(0,time[1]):
                n = r(1,prob1[1])
                if legend_leader_prob:
                    if n in range(1,legend_leader_prob+1):
                        leadercard.append(r1(legend_leader_card))
                        continue
                if only_leader:
                    pass
                if legend_alternate_prob:
                    if n in range(legend_leader_prob+1,legend_leader_prob+legend_alternate_prob+1):
                        card[1].append(r1(legend_alternate_card))
                        continue
                card[1].append(r1(cards[1]))
        if time[2]:
            for i in range(0,time[2]):
                n = r(1,prob1[2])
                if gold_leader_prob:
                    if n in range(1,gold_leader_prob+1):
                        leadercard.append(r1(gold_leader_card))
                        continue
                if only_legend:
                    continue
                if gold_alternate_prob:
                    if n in range(gold_leader_prob+1,gold_leader_prob+gold_alternate_prob+1):
                        card[2].append(r1(gold_alternate_card))
                        continue
                card[2].append(r1(cards[2]))
        if time[3]:
            for i in range(0,time[3]):
                n = r(1,prob2[3]) if no_bronze else r(1,prob1[3])
                if silver_leader_prob:
                    if n in range(1,silver_leader_prob+1):
                        leadercard.append(r1(silver_leader_card))
                        continue
                if only_legend:
                    continue
                if silver_alternate_prob:
                    if n in range(silver_leader_prob+1,silver_leader_prob+silver_alternate_prob+1):
                        card[3].append(r1(silver_alternate_card))
                        continue
                card[3].append(r1(cards[3]))
        if time[4]:
            for i in range(0,time[4]):
                n = r(1,prob1[4])
                if bronze_leader_prob:
                    if n in range(1,bronze_leader_prob+1):
                        leadercard.append(r1(bronze_leader_card))
                        continue
                if only_legend:
                    continue
                if bronze_alternate_prob:
                    if n in range(bronze_leader_prob+1,bronze_leader_prob+bronze_alternate_prob+1):
                        card[4].append(r1(bronze_alternate_card))
                        continue
                card[4].append(r1(cards[4]))
    return leadercard,card
                
async def gachaing(card_set:int,time:int,only_leader:bool) -> str:
    """
    抽卡,返回结果
    """
    leader,alternate,cards = get_card_set(card_set)
    result = {1:0,2:0,3:0,4:0}
    result2 = {1:0,2:0,3:0,4:0}
    for i in range(0,7*time):
        n = r(1,prob1[4])
        for rare in range(1,5):
            if n <= prob1[rare]:
                result[rare] += 1
                break
    for i in range(0,time):
        n = r(1,prob2[4])
        for rare in range(1,5):
            if n <= prob2[rare]:
                result2[rare] += 1
                break
    leadercard,card = await rolls(result,leader,alternate,cards,only_leader,False,False)
    leadercard1,card1 = await rolls(result2,leader,alternate,cards,only_leader,False,True)
    for i in leadercard1:
        leadercard.append(i)
    for i in card1:
        for j in card1[i]:
            card[i].append(j)
    result = {1:result[1]+result2[1],2:result[2]+result2[2],3:result[3]+result2[3],4:result[4]+result2[4]}
    return leadercard,card,result
    
    
    