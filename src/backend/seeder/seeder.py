from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.bank.crud import bank_dao
from src.backend.bank.schemas import BankAddRequest
from src.backend.card.schemas import CardAddRequest
from src.backend.card.crud import card_dao

class Seeder:
    async def seed_initial_data(self, db: AsyncSession):
        banks = await bank_dao.get_all(db)
        if banks.__len__() > 0:
            return
        bank_data = {
    "banks": [
        {
            "name": "Chase",
            "logo_url": "https://www.chase.com/etc/designs/chase-ux/css/img/newheaderlogo.svg",
            "website": "https://www.chase.com",
            "cards": [
                {
                    "name": "Chase Sapphire Preferred",
                    "description": "Travel rewards card with generous sign-up bonus",
                    "annual_fee": 95,
                    "reward_desc": "2x on travel/dining, 1x on all else",
                    "interest_rate": 2149,
                    "min_credit_score": 700
                },
                {
                    "name": "Chase Freedom Unlimited",
                    "description": "Cash back card with no annual fee",
                    "annual_fee": 0,
                    "reward_desc": "1.5% cash back on all purchases",
                    "interest_rate": 2024,
                    "min_credit_score": 670
                },
                {
                    "name": "Chase Amazon Prime Rewards",
                    "description": "Co-branded card for Amazon shoppers",
                    "annual_fee": 0,
                    "reward_desc": "5% back at Amazon/Whole Foods, 2% at restaurants/gas stations/drugstores",
                    "interest_rate": 1949,
                    "min_credit_score": 680
                }
            ]
        },
        {
            "name": "American Express",
            "logo_url": "https://www.aexp-static.com/cdaas/one/statics/axp-static-assets/1.8.0/package/dist/img/logos/dls-logo-bluebox-solid.svg",
            "website": "https://www.americanexpress.com",
            "cards": [
                {
                    "name": "Amex Platinum",
                    "description": "Premium travel card with luxury benefits",
                    "annual_fee": 695,
                    "reward_desc": "5x on flights, 5x on prepaid hotels, 1x on other purchases",
                    "interest_rate": 2199,
                    "min_credit_score": 720
                },
                {
                    "name": "Amex Gold",
                    "description": "Rewards card focused on dining and groceries",
                    "annual_fee": 250,
                    "reward_desc": "4x at restaurants/U.S. supermarkets, 3x on flights, 1x on other purchases",
                    "interest_rate": 2099,
                    "min_credit_score": 700
                },
                {
                    "name": "Amex Blue Cash Preferred",
                    "description": "Cash back card for everyday spending",
                    "annual_fee": 95,
                    "reward_desc": "6% at U.S. supermarkets (up to $6k/year), 6% on streaming, 3% at transit/gas stations",
                    "interest_rate": 1924,
                    "min_credit_score": 680
                }
            ]
        },
        {
            "name": "Citi",
            "logo_url": "https://www.citi.com/CBOL/IA/Angular/assets/citiredesign.svg",
            "website": "https://www.citi.com",
            "cards": [
                {
                    "name": "Citi Double Cash",
                    "description": "Simple cash back card",
                    "annual_fee": 0,
                    "reward_desc": "2% cash back (1% when you buy, 1% when you pay)",
                    "interest_rate": 1924,
                    "min_credit_score": 670
                },
                {
                    "name": "Citi Premier",
                    "description": "Travel rewards card with flexible points",
                    "annual_fee": 95,
                    "reward_desc": "3x on restaurants/supermarkets/gas stations/air travel/hotels",
                    "interest_rate": 2124,
                    "min_credit_score": 700
                },
                {
                    "name": "Citi Custom Cash",
                    "description": "Card that automatically earns highest cash back",
                    "annual_fee": 0,
                    "reward_desc": "5% cash back in top eligible spend category (up to $500 per billing cycle), 1% thereafter",
                    "interest_rate": 1924,
                    "min_credit_score": 680
                }
            ]
        },
        {
            "name": "Capital One",
            "logo_url": "https://www.capitalone.com/logo/logo-standard@2x.png",
            "website": "https://www.capitalone.com",
            "cards": [
                {
                    "name": "Capital One Venture X",
                    "description": "Premium travel rewards card",
                    "annual_fee": 395,
                    "reward_desc": "2x miles on all purchases, 5x on flights, 10x on hotels/rental cars",
                    "interest_rate": 2199,
                    "min_credit_score": 720
                },
                {
                    "name": "Capital One SavorOne",
                    "description": "Cash back card for dining and entertainment",
                    "annual_fee": 0,
                    "reward_desc": "3% on dining/entertainment/grocery stores, 1% on other purchases",
                    "interest_rate": 1999,
                    "min_credit_score": 670
                },
                {
                    "name": "Capital One Quicksilver",
                    "description": "Simple cash back card with no annual fee",
                    "annual_fee": 0,
                    "reward_desc": "1.5% cash back on all purchases",
                    "interest_rate": 1999,
                    "min_credit_score": 660
                }
            ]
        }
    ]
}
        
        for bank_info in bank_data["banks"]:
            bank = BankAddRequest.model_validate(bank_info)
            bank_dict = bank.model_dump()
            await bank_dao.create(db, bank_dict)
            await db.flush()
            new_bank = await bank_dao.get_by_name(db, bank.name)
            for card_info in bank_info["cards"]:
                card_info["bank_id"] = new_bank.id
                card = CardAddRequest.model_validate(card_info)
                card_dict = card.model_dump()
                await card_dao.create(db, card_dict)
                await db.flush()

        await db.commit()

seeder: Seeder = Seeder()