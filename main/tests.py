from django.test import TestCase
from .models import NiceThing
from django.urls import reverse

class ViewTests(TestCase):

    def test_index_view(self):
        nice_thing = NiceThing.objects.create(
            text = "Something nice happened today"
        )
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("main/index.html")
        self.assertContains(response, "Something nice happened today")

    def test_share_page_initial(self):
        nice_thing = NiceThing.objects.create(
            text = "Something nice happened today"
        )
        response = self.client.get(reverse("thing", 
                                    kwargs={"nice_thing_id": nice_thing.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("main/thing.html")
        self.assertContains(response, "Something nice happened today")

    def test_add_nice_thing(self):
        response = self.client.get(reverse("add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("main/add.html")

        form = response.context["form"]
        data = form.initial
        data["text"] = "Adding a nice thing"

        self.assertEqual(NiceThing.objects.count(), 0)

        response = self.client.post(
            reverse("add"),
            data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/thing.html")
        self.assertContains(response, "Adding a nice thing")
        self.assertEqual(NiceThing.objects.count(), 1)

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), "NiceThing added. Thank you.")


    def test_report_nice_thing(self):
        nice_thing = NiceThing.objects.create(
            text = "Something nice happened today"
        )

        response = self.client.get(reverse("report",
                                    kwargs={"nice_thing_id": nice_thing.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("main/report.html")

        form = response.context["form"]
        data = form.initial
        data["reported_reason"] = "Not very nice"

        response = self.client.post(
            reverse("report", kwargs={"nice_thing_id": nice_thing.id}),
            data,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        
        # check database contains reported=True
        nice_thing = NiceThing.objects.get(id=nice_thing.id)
        self.assertEqual(nice_thing.reported, True)
        self.assertEqual(nice_thing.reported_reason, "Not very nice")

        messages = list(response.context["messages"])
        self.assertEqual(str(messages[0]), 
                        "NiceThing reported and will be reviewed. Thank you.")
