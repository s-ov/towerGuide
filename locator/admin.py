from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (DistributiveSubstation as DS,
                     MotorControlCenter as MCC, 
                     Node
                    )


@admin.register(DS)
class DSAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'level',]
    list_display = ('title', 'slug', 'level',)
    prepopulated_fields = {"slug": ("title", )}
    list_display_links = ('title', )
    ordering = ['title']


@admin.register(MCC)
class DSAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'substation',]
    list_display = ('title', 'slug', 'substation',)
    prepopulated_fields = {"slug": ("title", )}
    list_display_links = ('title', )
    ordering = ['title']


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'label_photo', 'label', 'level', 'round_per_minute', 'power', 'mcc']
    list_display = ('title', 'slug', 'label', 'round_per_minute', 'power', 'mcc',)
    readonly_fields = ['label_photo']
    list_display_links = ('title', )
    ordering = ['slug']
    save_on_top = True

    @admin.display(description="Image", ordering='title')
    def label_photo(self, node: Node):
        if node.label:
            return mark_safe(f"<img src='{node.label.url}' width=50>")
        return "No image"
