# Filament v5.6.5 — Verified Developer Reference

> Source-verified from `vendor/filament` — NOT from blog posts or v3 docs
>
> SajiloMart · Code IT Intern Group C · May 2026

---

## 1. Verified Class Namespaces (v5.6.5)

### 1.1 Form Components

| Namespace (CORRECT) | Component |
|---------------------|-----------|
| `Filament\Forms\Components\TextInput` | TextInput field |
| `Filament\Forms\Components\Select` | Dropdown select |
| `Filament\Forms\Components\Toggle` | Boolean toggle |
| `Filament\Forms\Components\FileUpload` | File/image upload |
| `Filament\Forms\Components\Textarea` | Multi-line text |
| `Filament\Forms\Components\DatePicker` | Date picker |
| `Filament\Forms\Components\RichEditor` | WYSIWYG editor |

### 1.2 Layout Components — CRITICAL CHANGE FROM v3

> ⚠️ **BREAKING CHANGE:** `Section` is NO LONGER in `Filament\Forms\Components\`. It moved to `Filament\Schemas\Components\` in v5.

| Namespace (CORRECT) | Component |
|---------------------|-----------|
| `Filament\Schemas\Components\Section` | Section wrapper (NOT Forms\Components) |
| `Filament\Schemas\Components\Grid` | Grid layout |
| `Filament\Schemas\Components\Tabs` | Tabbed layout |
| `Filament\Schemas\Components\Wizard` | Multi-step wizard |
| `Filament\Schemas\Schema` | Schema class itself |

### 1.3 Table Components

| Namespace (CORRECT) | Component |
|---------------------|-----------|
| `Filament\Tables\Columns\TextColumn` | Text column |
| `Filament\Tables\Columns\ImageColumn` | Image column |
| `Filament\Tables\Columns\IconColumn` | Icon/boolean column |
| `Filament\Tables\Columns\BadgeColumn` | Badge column |
| `Filament\Tables\Filters\SelectFilter` | Select dropdown filter |
| `Filament\Tables\Filters\TernaryFilter` | True/false/all filter |
| `Filament\Tables\Filters\TrashedFilter` | Soft delete filter |
| `Filament\Tables\Table` | Table class |

### 1.4 Actions — CRITICAL CHANGE FROM v3

> ⚠️ **BREAKING CHANGE:** All actions (Edit, Delete, BulkActionGroup) moved to `Filament\Actions\`. Never import from `Filament\Tables\Actions\`.

| Namespace (CORRECT) | Action |
|---------------------|--------|
| `Filament\Actions\EditAction` | Edit record action |
| `Filament\Actions\DeleteAction` | Delete record action |
| `Filament\Actions\BulkActionGroup` | Bulk action group |
| `Filament\Actions\DeleteBulkAction` | Bulk delete action |
| `Filament\Actions\ForceDeleteBulkAction` | Bulk force delete |
| `Filament\Actions\RestoreBulkAction` | Bulk restore (soft delete) |

---

## 2. Verified Method Signatures (v5.6.5)

### 2.1 Resource Shell — form() and table()

> ✅ **VERIFIED:** In v5.6.5, `form()` uses `Schema` not `Form`. This is different from what older docs say.

```php
// ✅ CORRECT — verified from Resource.php line 58 & 68
public static function form(Schema $schema): Schema  // NOT Form $form
public static function table(Table $table): Table    // Table unchanged

// Required imports in Resource shell:
use Filament\Schemas\Schema;
use Filament\Tables\Table;
```

### 2.2 Schema File (Schemas/ModelForm.php)

```php
// ✅ CORRECT — Schema has both methods, use either:
public static function configure(Schema $schema): Schema
{
    return $schema->schema([...]);      // ->schema() works
    // OR
    return $schema->components([...]);  // ->components() also works
}

// Required import:
use Filament\Schemas\Schema;
```

### 2.3 Table File (Tables/ModelsTable.php)

```php
// ✅ CORRECT — verified method names:
->recordActions([...])   // per-row actions (Edit, Delete)
->actions([...])         // alias for recordActions — both work
->toolbarActions([...])  // toolbar-level actions
->bulkActions([...])     // bulk selection actions
->headerActions([...])   // header area actions

// BulkActions go in ->bulkActions(), NOT ->toolbarActions()
```

---

## 3. Complete File Templates (Copy-Paste Safe)

### 3.1 Resource Shell — ModelResource.php

```php
<?php

namespace App\Filament\Resources\Models;

use App\Filament\Resources\Models\Pages\CreateModel;
use App\Filament\Resources\Models\Pages\EditModel;
use App\Filament\Resources\Models\Pages\ListModels;
use App\Filament\Resources\Models\Schemas\ModelForm;
use App\Filament\Resources\Models\Tables\ModelsTable;
use App\Models\Model;
use Filament\Resources\Resource;
use Filament\Schemas\Schema;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Model as EloquentModel;

class ModelResource extends Resource
{
    protected static ?string $model = Model::class;
    // ONLY $model here. No navigation properties.

    public static function getNavigationGroup(): string|null
    {
        return 'Catalog'; // use method, never property
    }

    public static function getNavigationIcon(): string|null
    {
        return 'heroicon-o-tag'; // use method, never property
    }

    public static function form(Schema $schema): Schema
    {
        return ModelForm::configure($schema);
    }

    public static function table(Table $table): Table
    {
        return ModelsTable::configure($table);
    }

    public static function getPages(): array
    {
        return [
            'index'  => ListModels::route('/'),
            'create' => CreateModel::route('/create'),
            'edit'   => EditModel::route('/{record}/edit'),
        ];
    }

    // DEVELOPMENT: return true. PRODUCTION: use ->can()
    public static function canViewAny(): bool { return true; }
    public static function canCreate(): bool { return true; }
    public static function canEdit(EloquentModel $r): bool { return true; }
    public static function canDelete(EloquentModel $r): bool { return true; }
}
```

### 3.2 Schema File — Schemas/ModelForm.php

```php
<?php

namespace App\Filament\Resources\Models\Schemas;

use App\Models\Category;
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Section;  // ← Schemas not Forms
use Filament\Schemas\Schema;
use Illuminate\Support\Str;

class ModelForm
{
    public static function configure(Schema $schema): Schema
    {
        return $schema->schema([
            Section::make('Details')
                ->columns(2)
                ->schema([
                    TextInput::make('name')
                        ->required()
                        ->live(onBlur: true)
                        ->afterStateUpdated(fn($s, callable $set) =>
                            $set('slug', Str::slug($s))
                        ),
                    TextInput::make('slug')
                        ->required(),
                    Select::make('category_id')
                        ->relationship('category', 'name')
                        ->searchable()->preload()->nullable(),
                    Toggle::make('is_active')->default(true),
                    FileUpload::make('image')
                        ->image()->directory('models'),
                ]),
        ]);
    }
}
```

### 3.3 Table File — Tables/ModelsTable.php

```php
<?php

namespace App\Filament\Resources\Models\Tables;

use Filament\Actions\BulkActionGroup;       // ← Filament\Actions not Tables
use Filament\Actions\DeleteBulkAction;      // ← Filament\Actions not Tables
use Filament\Actions\EditAction;            // ← Filament\Actions not Tables
use Filament\Actions\DeleteAction;          // ← Filament\Actions not Tables
use Filament\Tables\Columns\IconColumn;
use Filament\Tables\Columns\ImageColumn;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Filters\SelectFilter;
use Filament\Tables\Filters\TernaryFilter;
use Filament\Tables\Table;

class ModelsTable
{
    public static function configure(Table $table): Table
    {
        return $table
            ->columns([
                ImageColumn::make('image')->square()->size(40),
                TextColumn::make('name')->searchable()->sortable(),
                TextColumn::make('slug')->toggleable(isToggledHiddenByDefault: true),
                IconColumn::make('is_active')->boolean()->sortable(),
                TextColumn::make('created_at')->dateTime()->sortable()
                    ->toggleable(isToggledHiddenByDefault: true),
            ])
            ->filters([
                TernaryFilter::make('is_active'),
                SelectFilter::make('category_id')
                    ->relationship('category', 'name')
                    ->searchable()->preload(),
            ])
            ->recordActions([          // per-row actions
                EditAction::make(),
                DeleteAction::make(),
            ])
            ->bulkActions([            // bulk selection actions
                BulkActionGroup::make([
                    DeleteBulkAction::make(),
                ]),
            ]);
    }
}
```

---

## 4. v3 vs v5 Breaking Changes Cheatsheet

| v3 (WRONG — causes fatal errors) | v5.6.5 (CORRECT) |
|-----------------------------------|------------------|
| `Filament\Forms\Components\Section` | `Filament\Schemas\Components\Section` |
| `Filament\Tables\Actions\EditAction` | `Filament\Actions\EditAction` |
| `Filament\Tables\Actions\DeleteAction` | `Filament\Actions\DeleteAction` |
| `Filament\Tables\Actions\BulkActionGroup` | `Filament\Actions\BulkActionGroup` |
| `public static function form(Form $form): Form` | `public static function form(Schema $schema): Schema` |
| `->actions([EditAction])` | `->recordActions([EditAction])` or `->actions()` |
| `protected static ?string $navigationGroup` | `getNavigationGroup(): string\|null` method |
| `protected static ?string $navigationIcon` | `getNavigationIcon(): string\|null` method |
| `use Filament\Forms\Form` in Resource | `use Filament\Schemas\Schema` in Resource |

---

## 5. Navigation — Safe Pattern

> ⚠️ **RULE:** Never declare `$navigationGroup` or `$navigationIcon` as properties. Always use methods.

```php
// ✅ CORRECT — methods only, no properties
public static function getNavigationGroup(): string|null
{
    return 'Catalog';
}

public static function getNavigationIcon(): string|null
{
    return 'heroicon-o-tag';
}

public static function getNavigationSort(): ?int
{
    return 1;
}

// ❌ WRONG — all of these cause fatal PHP errors
protected static ?string $navigationGroup = 'Catalog';
protected static ?string $navigationIcon  = 'heroicon-o-tag';
protected static ?int    $navigationSort  = 1;
```

---

## 6. Common Errors & Exact Fixes

### Error: `Class Filament\Forms\Components\Section not found`

```php
// CAUSE: Section moved out of Forms in v5
// WRONG:
use Filament\Forms\Components\Section;
// CORRECT:
use Filament\Schemas\Components\Section;
```

### Error: `$navigationGroup must be UnitEnum|string|null`

```php
// CAUSE: Declared as property in Resource class
// WRONG:
protected static ?string $navigationGroup = 'Catalog';
// CORRECT:
public static function getNavigationGroup(): string|null { return 'Catalog'; }
```

### Error: `form() signature incompatible with Resource::form(Schema)`

```php
// CAUSE: Using Form type hint instead of Schema
// WRONG:
public static function form(Form $form): Form
// CORRECT:
public static function form(Schema $schema): Schema
// Import:
use Filament\Schemas\Schema;
```

### Error: `Class EditAction not found in Tables/ file`

```php
// CAUSE: Wrong namespace
// WRONG:
use Filament\Tables\Actions\EditAction;
// CORRECT:
use Filament\Actions\EditAction;
```

---

## 7. Artisan Commands

| Command | Purpose |
|---------|---------|
| `php artisan make:filament-resource Model --generate` | Generate full resource (shell + schemas + tables + pages) |
| `php artisan optimize:clear` | Clear all caches — run after every file change |
| `php artisan filament:cache-components` | Cache for production only |
| `php artisan filament:upgrade` | Run after `composer update` of filament |

> 📖 **Official Docs:** https://filamentphp.com/docs — If any example uses `Schema $schema` in a Form file, it is v3. Ignore it.
