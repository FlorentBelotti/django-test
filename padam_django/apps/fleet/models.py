from django.core.exceptions import ValidationError
from django.db import models


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):

    '''A shift during which a bus is driven by a driver. Joining the business side (driver, bus...)
    and the technical/geographic (place, busStop...) aspect of the data.'''

    # Relations Many-to-one: 1 shifts === 1 bus, but 1 bus === N shifts
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='shifts')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='shifts')

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"BusShift: {self.bus} {self.driver} {self.start_time} {self.end_time} (id: {self.pk})"

    def clean(self):

        # Validation: time consistency
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        # No overlapping bus shifts for the same bus or the same time.
        if self.bus_id and self.start_time and self.end_time:
            overlapping_bus_shifts = BusShift.objects.filter(
                bus=self.bus,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)
            if overlapping_bus_shifts.exists():
                raise ValidationError(f"Bus [{self.bus}] is already assigned to a shift.")

        # No overlapping driver shifts for the same driver or the same time.
        if self.driver_id and self.start_time and self.end_time:
            overlapping_driver_shifts = BusShift.objects.filter(
                driver=self.driver,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk)
            if overlapping_driver_shifts.exists():
                raise ValidationError(f"Driver [{self.driver}] is already assigned to a shift.")


class BusStop(models.Model):

    '''A stop made by a bus during a bus shift.'''

    # One-to-many relation: 1 busShift === N busStops, but 1 busStop === 1 busShift
    bus_shift = models.ForeignKey(BusShift, on_delete=models.CASCADE, related_name='stops')
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE)

    # Define order of stops within a bus shift
    order = models.IntegerField()

    stop_time = models.DateTimeField()

    # Auto ordering by 'order' field
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Stop {self.order}: {self.place.name} at {self.stop_time} (id: {self.pk})"
