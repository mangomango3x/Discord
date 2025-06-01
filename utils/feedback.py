import discord
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FeedbackManager:
    """Manages user feedback for fact-checking results"""

    def __init__(self):
        self.feedback_file = 'data/feedback.json'
        self.feedback_data = self.load_feedback()

    def load_feedback(self):
        """Load feedback data from file"""
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            os.makedirs('data', exist_ok=True)
            return {"feedback": [], "stats": {"helpful": 0, "not_helpful": 0}}

    def save_feedback(self):
        """Save feedback data to file"""
        try:
            os.makedirs('data', exist_ok=True)
            with open(self.feedback_file, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")

    def create_feedback_view(self, message_id, user_id):
        """Create a Discord view with feedback buttons"""
        return FeedbackView(self, message_id, user_id)

    def record_feedback(self, message_id, user_id, feedback_type, command_type=None):
        """
        Record user feedback

        Args:
            message_id (int): ID of the message being rated
            user_id (int): ID of the user providing feedback
            feedback_type (str): 'helpful' or 'not_helpful'
            command_type (str): Type of command ('expose', 'truthiness', etc.)
        """
        try:
            # Check if user already provided feedback for this message
            existing_feedback = None
            for feedback in self.feedback_data["feedback"]:
                if feedback["message_id"] == message_id and feedback["user_id"] == user_id:
                    existing_feedback = feedback
                    break

            if existing_feedback:
                # Update existing feedback
                old_type = existing_feedback["feedback_type"]
                existing_feedback["feedback_type"] = feedback_type
                existing_feedback["updated_at"] = datetime.utcnow().isoformat()

                # Update stats
                self.feedback_data["stats"][old_type] -= 1
                self.feedback_data["stats"][feedback_type] += 1
            else:
                # Add new feedback
                feedback_entry = {
                    "message_id": message_id,
                    "user_id": user_id,
                    "feedback_type": feedback_type,
                    "command_type": command_type,
                    "timestamp": datetime.utcnow().isoformat()
                }

                self.feedback_data["feedback"].append(feedback_entry)
                self.feedback_data["stats"][feedback_type] += 1

            self.save_feedback()
            return True

        except Exception as e:
            logger.error(f"Error recording feedback: {e}")
            return False

    def get_user_feedback(self, message_id, user_id):
        """Get existing feedback from a user for a specific message"""
        for feedback in self.feedback_data["feedback"]:
            if feedback["message_id"] == message_id and feedback["user_id"] == user_id:
                return feedback["feedback_type"]
        return None

    def get_feedback_stats(self):
        """Get overall feedback statistics"""
        return self.feedback_data["stats"].copy()

    def get_command_stats(self, command_type):
        """Get feedback statistics for a specific command type"""
        command_feedback = [f for f in self.feedback_data["feedback"] if f.get("command_type") == command_type]

        helpful = sum(1 for f in command_feedback if f["feedback_type"] == "helpful")
        not_helpful = sum(1 for f in command_feedback if f["feedback_type"] == "not_helpful")

        return {"helpful": helpful, "not_helpful": not_helpful}

class FeedbackView(discord.ui.View):
    """Discord UI View for feedback buttons"""

    def __init__(self, feedback_manager, message_id, user_id):
        super().__init__(timeout=300)  # 5 minute timeout
        self.feedback_manager = feedback_manager
        self.message_id = message_id
        self.user_id = user_id

        # Check if user already provided feedback
        existing_feedback = feedback_manager.get_user_feedback(message_id, user_id)

        # Update button styles based on existing feedback
        if existing_feedback == "helpful":
            self.helpful_button.style = discord.ButtonStyle.success
            self.not_helpful_button.style = discord.ButtonStyle.secondary
        elif existing_feedback == "not_helpful":
            self.helpful_button.style = discord.ButtonStyle.secondary
            self.not_helpful_button.style = discord.ButtonStyle.danger

    @discord.ui.button(label='👍 Helpful', style=discord.ButtonStyle.secondary, custom_id='helpful')
    async def helpful_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle helpful feedback"""
        await self.handle_feedback(interaction, "helpful")

    @discord.ui.button(label='👎 Not Helpful', style=discord.ButtonStyle.secondary, custom_id='not_helpful')
    async def not_helpful_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle not helpful feedback"""
        await self.handle_feedback(interaction, "not_helpful")

    async def handle_feedback(self, interaction: discord.Interaction, feedback_type):
        """Handle feedback button interaction"""
        try:
            # Record the feedback
            success = self.feedback_manager.record_feedback(
                self.message_id,
                interaction.user.id,
                feedback_type
            )

            if success:
                # Update button styles
                if feedback_type == "helpful":
                    self.helpful_button.style = discord.ButtonStyle.success
                    self.not_helpful_button.style = discord.ButtonStyle.secondary
                    message = "✅ Thank you for rating this analysis as helpful!"
                else:
                    self.helpful_button.style = discord.ButtonStyle.secondary
                    self.not_helpful_button.style = discord.ButtonStyle.danger
                    message = "📝 Thank you for your feedback. We'll work to improve our analysis!"

                # Update the view
                await interaction.response.edit_message(view=self)

                # Send ephemeral response
                await interaction.followup.send(message, ephemeral=True)

                # Log the feedback
                logger.info(f"User {interaction.user.id} rated message {self.message_id} as {feedback_type}")

            else:
                await interaction.response.send_message(
                    "❌ An error occurred while recording your feedback. Please try again.",
                    ephemeral=True
                )

        except Exception as e:
            logger.error(f"Error handling feedback: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while processing your feedback.",
                ephemeral=True
            )

    async def on_timeout(self):
        """Handle view timeout"""
        # Disable all buttons
        for item in self.children:
            item.disabled = True
