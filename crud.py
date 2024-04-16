import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from core.models import (
    User,
    db_helper,
    Profile,
    Post,
    Order,
    Product,
    OrderProductAssociation,
)


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print(user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return await session.scalar(stmt)


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    bio: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
    )
    session.add(profile)
    await session.commit()
    return profile


async def get_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user.profile)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print(user.posts)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    for post in posts:
        print(post)
        print(post.user)


async def get_users_with_posts_and_profiles(session: AsyncSession):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    for user in users:
        print(user, user.profile and user.profile.first_name)
        print(user.posts)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .where(User.username == "sam")
        .order_by(Profile.id)
    )
    profiles = await session.scalars(stmt)

    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def create_order(
    session: AsyncSession, total_sum: int, promocode: str | None = None
) -> Order:
    order = Order(promocode=promocode, total_sum=total_sum)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession, name: str, description: str, price: int
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order = await create_order(
        session,
        333,
    )
    order_promo = await create_order(session, 254, "NEW1000")

    keyboard = await create_product(
        session,
        "Razer Chroma",
        "RGB keyboard",
        199,
    )
    mouse = await create_product(
        session,
        "Razer Deathadder V3",
        "RGB mouse",
        299,
    )
    headphones = await create_product(
        session,
        "Razer Kraken 2024",
        "RGB headphones",
        399,
    )

    order = await session.scalar(
        select(Order).options(selectinload(Order.products)).where(Order.id == order.id)
    )
    order_promo = await session.scalar(
        select(Order)
        .options(selectinload(Order.products))
        .where(Order.id == order_promo.id)
    )
    order.products.append(mouse)
    order.products.append(keyboard)
    # order_promo.products.append(keyboard)
    # order_promo.products.append(headphones)
    order_promo.products = [keyboard, headphones]

    await session.commit()


async def create_orders_and_products_with_assoc(session: AsyncSession):
    order = await create_order(
        session,
        333,
    )
    order_promo = await create_order(session, 254, "NEW1000")

    keyboard = await create_product(
        session,
        "Razer Chroma",
        "RGB keyboard",
        199,
    )
    mouse = await create_product(
        session,
        "Razer Deathadder V3",
        "RGB mouse",
        299,
    )
    headphones = await create_product(
        session,
        "Razer Kraken 2024",
        "RGB headphones",
        399,
    )

    order = await session.scalar(
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .where(Order.id == order.id)
    )

    order_promo = await session.scalar(
        select(Order)
        .options(
            selectinload(Order.products_details).joinedload(
                OrderProductAssociation.product
            )
        )
        .where(Order.id == order_promo.id)
    )

    orders = [order, order_promo]

    for ordero in orders:
        ordero.products_details.append(
            OrderProductAssociation(product=mouse, count=2, unit_price=399)
        )

    order.products_details.append(
        OrderProductAssociation(product=keyboard, count=1, unit_price=200)
    )
    order_promo.products_details.append(
        OrderProductAssociation(product=headphones, count=5, unit_price=1999)
    )
    await session.commit()


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    return list(
        await session.scalars(
            select(Order).options(selectinload(Order.products)).order_by(Order.id)
        )
    )


async def get_orders_with_products_details(session: AsyncSession) -> list[Order]:
    return list(
        await session.scalars(
            select(Order)
            .options(
                selectinload(Order.products_details).joinedload(
                    OrderProductAssociation.product
                )
            )
            .order_by(Order.id)
        )
    )


async def print_orders_with_products_through_secondary(session: AsyncSession):
    orders = await get_orders_with_products(session)
    for order in orders:
        print(order.id, order.created_at, order.promocode)
        print(
            f"products: {[(product.id, product.name, product.price) for product in order.products]}"
        )


async def print_orders_with_products_with_association(session: AsyncSession):
    orders = await get_orders_with_products_details(session)
    for order in orders:
        print(order.id, order.created_at, order.promocode)
        print(
            f"products: {[(product_details.product.id, product_details.product.name, product_details.product.price, product_details.count) for product_details in order.products_details]}"
        )


async def add_tea_product_to_existing_order_assoc(session: AsyncSession):
    orders = await get_orders_with_products_details(session)
    tea = await create_product(
        session,
        "Tea",
        "Green tea",
        400,
    )
    for order in orders:
        order.products_details.append(
            OrderProductAssociation(product=tea, count=2, unit_price=399)
        )
    await session.commit()


# async def main_relations(session: AsyncSession):
#     await create_user(session, "no_posts")
#     await create_user(session, "josh")
#     user_sam = await get_user_by_username(session, "sam")
#     user_josh = await get_user_by_username(session, "sam")
#     print("Found user", username, user)
#     await create_user_profile(session, 2, first_name="Josh", last_name="Sepiol")
#     print(profile)
#     await get_users_with_profiles(session)
#     await create_posts(session, user_sam.id, "SQL2", "SQL1", "SQL0")
#     await create_posts(session, user_josh.id, "FASTAPI3", "FASTAPI1", "FASTAPI2")
#     await get_profiles_with_users_and_users_with_posts(session)


async def demo_m2m(session: AsyncSession):
    await print_orders_with_products_with_association(session)
    # await add_tea_product_to_existing_order_assoc(session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
