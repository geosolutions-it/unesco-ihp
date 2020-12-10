# Generated by Django 2.2.11 on 2020-04-02 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ihp_survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_user+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='survey',
            name='country',
            field=models.CharField(blank=True, choices=[('AFG', 'Afghanistan'), ('ALA', 'Aland Islands'), ('ALB', 'Albania'), ('DZA', 'Algeria'), ('ASM', 'American Samoa'), ('AND', 'Andorra'), ('AGO', 'Angola'), ('AIA', 'Anguilla'), ('ATG', 'Antigua and Barbuda'), ('ARG', 'Argentina'), ('ARM', 'Armenia'), ('ABW', 'Aruba'), ('AUS', 'Australia'), ('AUT', 'Austria'), ('AZE', 'Azerbaijan'), ('BHS', 'Bahamas'), ('BHR', 'Bahrain'), ('BGD', 'Bangladesh'), ('BRB', 'Barbados'), ('BLR', 'Belarus'), ('BEL', 'Belgium'), ('BLZ', 'Belize'), ('BEN', 'Benin'), ('BMU', 'Bermuda'), ('BTN', 'Bhutan'), ('BOL', 'Bolivia'), ('BIH', 'Bosnia and Herzegovina'), ('BWA', 'Botswana'), ('BRA', 'Brazil'), ('VGB', 'British Virgin Islands'), ('BRN', 'Brunei Darussalam'), ('BGR', 'Bulgaria'), ('BFA', 'Burkina Faso'), ('BDI', 'Burundi'), ('KHM', 'Cambodia'), ('CMR', 'Cameroon'), ('CAN', 'Canada'), ('CPV', 'Cape Verde'), ('CYM', 'Cayman Islands'), ('CAF', 'Central African Republic'), ('TCD', 'Chad'), ('CIL', 'Channel Islands'), ('CHL', 'Chile'), ('CHN', 'China'), ('HKG', 'China - Hong Kong'), ('MAC', 'China - Macao'), ('COL', 'Colombia'), ('COM', 'Comoros'), ('COG', 'Congo'), ('COK', 'Cook Islands'), ('CRI', 'Costa Rica'), ('CIV', "Cote d'Ivoire"), ('HRV', 'Croatia'), ('CUB', 'Cuba'), ('CYP', 'Cyprus'), ('CZE', 'Czech Republic'), ('PRK', "Democratic People's Republic of Korea"), ('COD', 'Democratic Republic of the Congo'), ('DNK', 'Denmark'), ('DJI', 'Djibouti'), ('DMA', 'Dominica'), ('DOM', 'Dominican Republic'), ('ECU', 'Ecuador'), ('EGY', 'Egypt'), ('SLV', 'El Salvador'), ('GNQ', 'Equatorial Guinea'), ('ERI', 'Eritrea'), ('EST', 'Estonia'), ('ETH', 'Ethiopia'), ('FRO', 'Faeroe Islands'), ('FLK', 'Falkland Islands (Malvinas)'), ('FJI', 'Fiji'), ('FIN', 'Finland'), ('FRA', 'France'), ('GUF', 'French Guiana'), ('PYF', 'French Polynesia'), ('GAB', 'Gabon'), ('GMB', 'Gambia'), ('GEO', 'Georgia'), ('DEU', 'Germany'), ('GHA', 'Ghana'), ('GIB', 'Gibraltar'), ('GRC', 'Greece'), ('GRL', 'Greenland'), ('GRD', 'Grenada'), ('GLP', 'Guadeloupe'), ('GUM', 'Guam'), ('GTM', 'Guatemala'), ('GGY', 'Guernsey'), ('GIN', 'Guinea'), ('GNB', 'Guinea-Bissau'), ('GUY', 'Guyana'), ('HTI', 'Haiti'), ('VAT', 'Holy See (Vatican City)'), ('HND', 'Honduras'), ('HUN', 'Hungary'), ('ISL', 'Iceland'), ('IND', 'India'), ('IDN', 'Indonesia'), ('IRN', 'Iran'), ('IRQ', 'Iraq'), ('IRL', 'Ireland'), ('IMN', 'Isle of Man'), ('ISR', 'Israel'), ('ITA', 'Italy'), ('JAM', 'Jamaica'), ('JPN', 'Japan'), ('JEY', 'Jersey'), ('JOR', 'Jordan'), ('KAZ', 'Kazakhstan'), ('KEN', 'Kenya'), ('KIR', 'Kiribati'), ('KWT', 'Kuwait'), ('KGZ', 'Kyrgyzstan'), ('LAO', "Lao People's Democratic Republic"), ('LVA', 'Latvia'), ('LBN', 'Lebanon'), ('LSO', 'Lesotho'), ('LBR', 'Liberia'), ('LBY', 'Libyan Arab Jamahiriya'), ('LIE', 'Liechtenstein'), ('LTU', 'Lithuania'), ('LUX', 'Luxembourg'), ('MKD', 'Macedonia'), ('MDG', 'Madagascar'), ('MWI', 'Malawi'), ('MYS', 'Malaysia'), ('MDV', 'Maldives'), ('MLI', 'Mali'), ('MLT', 'Malta'), ('MHL', 'Marshall Islands'), ('MTQ', 'Martinique'), ('MRT', 'Mauritania'), ('MUS', 'Mauritius'), ('MYT', 'Mayotte'), ('MEX', 'Mexico'), ('FSM', 'Micronesia, Federated States of'), ('MCO', 'Monaco'), ('MNG', 'Mongolia'), ('MNE', 'Montenegro'), ('MSR', 'Montserrat'), ('MAR', 'Morocco'), ('MOZ', 'Mozambique'), ('MMR', 'Myanmar'), ('NAM', 'Namibia'), ('NRU', 'Nauru'), ('NPL', 'Nepal'), ('NLD', 'Netherlands'), ('ANT', 'Netherlands Antilles'), ('NCL', 'New Caledonia'), ('NZL', 'New Zealand'), ('NIC', 'Nicaragua'), ('NER', 'Niger'), ('NGA', 'Nigeria'), ('NIU', 'Niue'), ('NFK', 'Norfolk Island'), ('MNP', 'Northern Mariana Islands'), ('NOR', 'Norway'), ('PSE', 'Occupied Palestinian Territory'), ('OMN', 'Oman'), ('PAK', 'Pakistan'), ('PLW', 'Palau'), ('PAN', 'Panama'), ('PNG', 'Papua New Guinea'), ('PRY', 'Paraguay'), ('PER', 'Peru'), ('PHL', 'Philippines'), ('PCN', 'Pitcairn'), ('POL', 'Poland'), ('PRT', 'Portugal'), ('PRI', 'Puerto Rico'), ('QAT', 'Qatar'), ('KOR', 'Republic of Korea'), ('MDA', 'Republic of Moldova'), ('REU', 'Reunion'), ('ROU', 'Romania'), ('RUS', 'Russian Federation'), ('RWA', 'Rwanda'), ('BLM', 'Saint-Barthelemy'), ('SHN', 'Saint Helena'), ('KNA', 'Saint Kitts and Nevis'), ('LCA', 'Saint Lucia'), ('MAF', 'Saint-Martin (French part)'), ('SPM', 'Saint Pierre and Miquelon'), ('VCT', 'Saint Vincent and the Grenadines'), ('WSM', 'Samoa'), ('SMR', 'San Marino'), ('STP', 'Sao Tome and Principe'), ('SAU', 'Saudi Arabia'), ('SEN', 'Senegal'), ('SRB', 'Serbia'), ('SYC', 'Seychelles'), ('SLE', 'Sierra Leone'), ('SGP', 'Singapore'), ('SVK', 'Slovakia'), ('SVN', 'Slovenia'), ('SLB', 'Solomon Islands'), ('SOM', 'Somalia'), ('ZAF', 'South Africa'), ('SSD', 'South Sudan'), ('ESP', 'Spain'), ('LKA', 'Sri Lanka'), ('SDN', 'Sudan'), ('SUR', 'Suriname'), ('SJM', 'Svalbard and Jan Mayen Islands'), ('SWZ', 'Swaziland'), ('SWE', 'Sweden'), ('CHE', 'Switzerland'), ('SYR', 'Syrian Arab Republic'), ('TJK', 'Tajikistan'), ('THA', 'Thailand'), ('TLS', 'Timor-Leste'), ('TGO', 'Togo'), ('TKL', 'Tokelau'), ('TON', 'Tonga'), ('TTO', 'Trinidad and Tobago'), ('TUN', 'Tunisia'), ('TUR', 'Turkey'), ('TKM', 'Turkmenistan'), ('TCA', 'Turks and Caicos Islands'), ('TUV', 'Tuvalu'), ('UGA', 'Uganda'), ('UKR', 'Ukraine'), ('ARE', 'United Arab Emirates'), ('GBR', 'United Kingdom'), ('TZA', 'United Republic of Tanzania'), ('USA', 'United States of America'), ('VIR', 'United States Virgin Islands'), ('URY', 'Uruguay'), ('UZB', 'Uzbekistan'), ('VUT', 'Vanuatu'), ('VEN', 'Venezuela (Bolivarian Republic of)'), ('VNM', 'Viet Nam'), ('WLF', 'Wallis and Futuna Islands'), ('ESH', 'Western Sahara'), ('YEM', 'Yemen'), ('ZMB', 'Zambia'), ('ZWE', 'Zimbabwe')], help_text='country of the physical address', max_length=3, null=True, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='organization',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='reason_for_data_download',
            field=models.TextField(verbose_name='Reason for data download'),
        ),
        migrations.AlterField(
            model_name='surveyconfiguration',
            name='cookie_expiration_time',
            field=models.IntegerField(default=24, verbose_name='Cookie expiration time in hours'),
        ),
    ]
