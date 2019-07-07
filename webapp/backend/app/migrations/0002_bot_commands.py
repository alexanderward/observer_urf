from django.db import migrations
commands = [
    dict(name="!blue <amount>", description="Bet X on blue team"),
    dict(name="!red <amount>", description="Bet X on red team"),
    dict(name="!gameinfo", description="Match details"),
    dict(name="!balance", description="Your Balance"),
    dict(name="!free", description="Get free points.  Usable once a game."),
]

def insert(apps, schema_editor):
    BotCommand = apps.get_model('app', 'BotCommand')
    for command in commands:
        BotCommand.objects.create(**command)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert, reverse_code=migrations.RunPython.noop),
    ]
