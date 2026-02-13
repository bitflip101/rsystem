from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Asset, OrgUnit
from .forms import AssetForm, OrgUnitForm
from staffing.models import Employee # To support the "Staff" button

def is_admin_or_manager(user):
    return user.is_staff or (hasattr(user, 'employees') and user.employee.position.rank_level >= 8)

@login_required
@user_passes_test(is_admin_or_manager)
def org_management_dashboard(request):
    assets = Asset.objects.prefetch_related('units').all()

    context = {
        'assets': assets,
        'total_units': OrgUnit.objects.count(),
    }
    tn = "core_org/mgmt_dashboard.html"
    return render(request, tn, context)

def asset_create(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core_org:dashboard')
    else:
        form = AssetForm()
    tn = "core_org/form_page.html"
    context = {'form': form, 'title': 'Register New Asset'}
    return render(request, tn, context)
        
def unit_add_to_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == "POST":
        form = OrgUnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.asset = asset # Force the asset to be the one we clicked on
            unit.save()
            return redirect('core_org:dashboard')

    else:
        ## Pre-fill the asset in the form
        form = OrgUnitForm(initial={'asset': asset})
    tn = "core_org/form_page.html"
    context = {'form': form, 'title': f"Add Unit to {asset.name}"}
    return render(request, tn, context)

def unit_edit(request, pk):
    unit = get_object_or_404(OrgUnit, pk=pk)
    form = OrgUnitForm(request.POST or None, instance=unit)

    if form.is_valid():
        form.save()
        return redirect('core_org:dashboard')
    tn = "core_org/form_page.html"
    context = {'form': form, 'title': f"Edit {unit.name}"}
    return render(request, tn, context)

def unit_staff_list(request, pk):
    unit = get_object_or_404(OrgUnit, pk=pk)
    # Find all employees whose position belongs to this unit
    staff = Employee.objects.filter(position__org_unit=unit)
    tn = "core_org/unit_staff.html"
    context = {'unit': unit, 'staff': staff}
    return render (request, tn ,context)

def org_explorer(request, asset_id=None, unit_id=None):
    context = {
        'current_asset': None,
        'current_unit': None,
        'breadcrumbs': [],
        'items': [], 
        'next_type': 'Asset',
    }

    ## Level 1: List all Assets
    if not asset_id and not unit_id:
        context['items'] = Asset.objects.all()
        context['next_type'] = 'Asset'
        context['title'] = "Regional Assets"
    
    ## Level 2: List Top-Level Units for an Asset (e.g., Corporate/Exex)
    elif asset_id and not unit_id:
        asset = get_object_or_404(Asset, id=asset_id)
        context['current_asset'] = asset
        context['items'] = OrgUnit.objects.filter(asset=asset, parent__isnull=True)
        context['next_type'] = 'Corporate/Executive Unit'
        context['breadcrumbs'] = [{'name': asset.get_name_display(), 'url': None}]
        context['title'] = f"Units in {asset.get_name_display()}"
    ## Level 3: List Sub-Units for a Parent Unit (Dept -> Div -> Group)
    elif unit_id:
        unit = get_object_or_404(OrgUnit, id=unit_id)
        context['current_unit'] = unit
        context['current_asset'] = unit.asset
        context['items'] = unit.sub_units.all()
        context['next_type'] = 'Sub-Unit'

        ## Build Breadcrumbs by recursing upwards
        crumbs = []
        curr = unit
        while curr:
            crumbs.insert(0, {'name': curr.name, 'id': curr.id})
            curr = curr.parent
        ## Add the Asset at the very start
        crumbs.insert(0, {'name': unit.asset.get_name_display(), 'asset_id': unit.asset.id})
        context['breadcrumbs'] = crumbs
        context['title'] = f"Inside {unit.name}"
    tn = "core_org/org_explorer.html"
    return render(request, tn, context)