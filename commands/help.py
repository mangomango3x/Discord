import discord
from discord.ext import commands
from config import COLORS, COMMAND_PREFIX

class HelpCog(commands.Cog):
    """Cog for help and information commands"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help', aliases=['h', 'commands'])
    async def help_command(self, ctx, command_name=None):
        """
        Shows help information for bot commands.
        
        Usage: !help [command]
        """
        if command_name:
            await self.show_command_help(ctx, command_name)
        else:
            await self.show_general_help(ctx)
    
    async def show_general_help(self, ctx):
        """Show general help with all commands"""
        embed = discord.Embed(
            title="🤖 Fact-Check Bot Help",
            description="AI-powered fact-checking and misinformation detection bot",
            color=COLORS["info"]
        )
        
        # Core Commands
        embed.add_field(
            name="🎯 Core Commands",
            value=(
                f"`{COMMAND_PREFIX}expose <statement>` - Expose misinformation with facts\n"
                f"`{COMMAND_PREFIX}truthiness <statement>` - Rate statement credibility (percentage)\n"
                f"`{COMMAND_PREFIX}help [command]` - Show this help or command details"
            ),
            inline=False
        )
        
        # AI Features
        embed.add_field(
            name="🤖 AI Features",
            value=(
                "• **Advanced Analysis** - ChatGPT powered fact-checking\n"
                "• **Credibility Scoring** - Percentage-based truthiness rating\n"
                "• **Context Awareness** - Understands nuanced statements\n"
                "• **Source Integration** - Cross-references reliable fact-checkers"
            ),
            inline=False
        )
        
        # Interactive Features
        embed.add_field(
            name="⚡ Interactive Features",
            value=(
                "• **Reply Detection** - Mention me in replies to fact-check messages\n"
                "• **Feedback Buttons** - Rate analyses as helpful or not helpful\n"
                "• **Confidence Bars** - Visual confidence indicators\n"
                "• **Rate Limiting** - Prevents spam (5 commands/minute)"
            ),
            inline=False
        )
        
        # Reliable Sources
        embed.add_field(
            name="📰 Trusted Sources",
            value=(
                "• **Snopes** - Fact-checking and debunking\n"
                "• **FactCheck.org** - Political fact-checking\n"
                "• **PolitiFact** - Political truth rating\n"
                "• **Reuters Fact Check** - News verification\n"
                "• **AP Fact Check** - Associated Press verification"
            ),
            inline=False
        )
        
        embed.set_footer(
            text=f"Use {COMMAND_PREFIX}help <command> for detailed command information",
            icon_url=ctx.bot.user.avatar.url if ctx.bot.user.avatar else None
        )
        
        await ctx.send(embed=embed)
    
    async def show_command_help(self, ctx, command_name):
        """Show detailed help for a specific command"""
        command_name = command_name.lower()
        
        if command_name in ['expose', 'fact', 'check']:
            embed = discord.Embed(
                title="🎯 Expose Command",
                description="Exposes misinformation by providing factual information",
                color=COLORS["success"]
            )
            
            embed.add_field(
                name="📝 Usage",
                value=f"`{COMMAND_PREFIX}expose <statement>`",
                inline=False
            )
            
            embed.add_field(
                name="📋 Aliases",
                value=f"`{COMMAND_PREFIX}fact`, `{COMMAND_PREFIX}check`",
                inline=False
            )
            
            embed.add_field(
                name="💡 Examples",
                value=(
                    f"`{COMMAND_PREFIX}expose vaccines cause autism`\n"
                    f"`{COMMAND_PREFIX}expose climate change is a hoax`\n"
                    f"`{COMMAND_PREFIX}expose 5G causes COVID-19`"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🔍 What it does",
                value=(
                    "• Analyzes the statement using AI\n"
                    "• Provides factual counter-information\n"
                    "• Shows credibility score with visual bar\n"
                    "• Cross-references reliable fact-checking sources\n"
                    "• Includes confidence level of the analysis"
                ),
                inline=False
            )
            
        elif command_name in ['truthiness', 'truth', 'rate', 'credibility']:
            embed = discord.Embed(
                title="📊 Truthiness Command",
                description="Rates the credibility of statements using AI analysis",
                color=COLORS["warning"]
            )
            
            embed.add_field(
                name="📝 Usage",
                value=f"`{COMMAND_PREFIX}truthiness <statement>`",
                inline=False
            )
            
            embed.add_field(
                name="📋 Aliases",
                value=f"`{COMMAND_PREFIX}truth`, `{COMMAND_PREFIX}rate`, `{COMMAND_PREFIX}credibility`",
                inline=False
            )
            
            embed.add_field(
                name="💡 Examples",
                value=(
                    f"`{COMMAND_PREFIX}truthiness the earth is flat`\n"
                    f"`{COMMAND_PREFIX}truthiness coffee is good for health`\n"
                    f"`{COMMAND_PREFIX}truthiness humans never landed on the moon`"
                ),
                inline=False
            )
            
            embed.add_field(
                name="🔍 What it does",
                value=(
                    "• Provides percentage-based truthiness rating\n"
                    "• Shows visual truthiness bar\n"
                    "• Explains AI reasoning behind the rating\n"
                    "• Categorizes the type of statement\n"
                    "• Includes confidence level and interpretation"
                ),
                inline=False
            )
            
        else:
            embed = discord.Embed(
                title="❌ Command Not Found",
                description=f"No help available for command: `{command_name}`",
                color=COLORS["error"]
            )
            
            embed.add_field(
                name="Available Commands",
                value=f"Use `{COMMAND_PREFIX}help` to see all available commands.",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='about', aliases=['info'])
    async def about_command(self, ctx):
        """Show information about the bot"""
        embed = discord.Embed(
            title="🤖 About Fact-Check Bot",
            description="An AI-powered Discord bot designed to combat misinformation",
            color=COLORS["info"]
        )
        
        embed.add_field(
            name="🎯 Purpose",
            value=(
                "This bot helps users identify and understand misinformation by providing "
                "fact-based analysis and credibility ratings using advanced AI technology."
            ),
            inline=False
        )
        
        embed.add_field(
            name="🧠 AI Technology",
            value=(
                "• **GPT-4o** - Latest OpenAI model for analysis\n"
                "• **Advanced Reasoning** - Context-aware fact-checking\n"
                "• **Multi-source Verification** - Cross-references multiple sources"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📊 Features",
            value=(
                "• Real-time fact-checking\n"
                "• Percentage-based truthiness ratings\n"
                "• Interactive feedback system\n"
                "• Reply-based fact-checking\n"
                "• Rate limiting for fair usage"
            ),
            inline=False
        )
        
        embed.add_field(
            name="🔒 Privacy & Security",
            value=(
                "• No personal data stored\n"
                "• Feedback data is anonymized\n"
                "• Rate limiting prevents abuse\n"
                "• Open source methodology"
            ),
            inline=False
        )
        
        embed.set_footer(
            text="Use !help to see available commands",
            icon_url=ctx.bot.user.avatar.url if ctx.bot.user.avatar else None
        )
        
        await ctx.send(embed=embed)

    @help_command.error
    async def help_error(self, ctx, error):
        """Handle help command errors"""
        await ctx.send("❌ An error occurred while showing help. Please try again.")
